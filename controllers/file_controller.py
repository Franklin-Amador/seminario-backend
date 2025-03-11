from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import shutil
from datetime import datetime
import uuid
from db import prisma_client as prisma

# Configurar la ruta para almacenar archivos
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Asegurarse de que existan subdirectorios para diferentes tipos de archivos
ASSIGNMENT_DIR = os.path.join(UPLOAD_DIR, "assignments")
RESOURCE_DIR = os.path.join(UPLOAD_DIR, "resources")
PROFILE_DIR = os.path.join(UPLOAD_DIR, "profiles")

for directory in [ASSIGNMENT_DIR, RESOURCE_DIR, PROFILE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)


# Router para manejo de archivos
router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)

# Endpoint para subir archivos de tareas
@router.post("/assignment/{assignment_id}")
async def upload_assignment_file(
    assignment_id: int,
    user_id: int,
    file: UploadFile = File(...),
):
    # Verificar si la tarea existe
    assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Verificar si el usuario está matriculado en el curso
    enrollment = await prisma.enrollment.find_first(
        where={
            "userid": user_id,
            "courseid": assignment.course,
            "status": 0  # Status activo
        }
    )
    if not enrollment:
        raise HTTPException(status_code=403, detail="User not enrolled in this course")
    
    # Crear un nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Crear directorio para la tarea si no existe
    assignment_submission_dir = os.path.join(ASSIGNMENT_DIR, str(assignment_id), str(user_id))
    if not os.path.exists(assignment_submission_dir):
        os.makedirs(assignment_submission_dir)
    
    # Guardar el archivo
    file_path = os.path.join(assignment_submission_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Crear o actualizar la entrega en la base de datos
    now = datetime.utcnow()
    submission_data = {
        "assignment": assignment_id,
        "userid": user_id,
        "timecreated": now,
        "timemodified": now,
        "status": "submitted",
        "attemptnumber": 0,
        "latest": True
    }
    
    # Buscar entregas previas
    existing_submission = await prisma.submission.find_first(
        where={
            "assignment": assignment_id,
            "userid": user_id
        }
    )
    
    if existing_submission:
        # Marcar la última entrega como no actual
        await prisma.submission.update_many(
            where={
                "assignment": assignment_id,
                "userid": user_id
            },
            data={"latest": False}
        )
        
        # Incrementar el número de intento
        submission_data["attemptnumber"] = existing_submission.attemptnumber + 1
    
    # Crear la nueva entrega
    new_submission = await prisma.submission.create(data=submission_data)
    
    return {
        "filename": file.filename,
        "stored_filename": unique_filename,
        "submission_id": new_submission.id,
        "message": "File uploaded successfully"
    }

# Endpoint para descargar archivo de tarea
@router.get("/assignment/{assignment_id}/{submission_id}")
async def download_assignment_file(
    assignment_id: int,
    submission_id: int,
    user_id: int = None
):
    # Verificar si la entrega existe
    submission = await prisma.submission.find_unique(where={"id": submission_id})
    if not submission or submission.assignment != assignment_id:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Verificar permisos si se proporciona user_id
    if user_id and submission.userid != user_id:
        # Verificar si el usuario es un profesor
        assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        # Obtener roles del usuario en el contexto del curso
        user_roles = await prisma.userrole.find_many(
            where={
                "userid": user_id,
                "contextid": assignment.course  # Asumiendo que contextid representa el curso
            },
            include={"role": True}
        )
        
        # Verificar si el usuario tiene rol de profesor
        is_teacher = False
        for user_role in user_roles:
            if user_role.role.shortname in ["teacher", "editingteacher"]:
                is_teacher = True
                break
        
        if not is_teacher:
            raise HTTPException(status_code=403, detail="Not authorized to access this submission")
    
    # Buscar el archivo en el directorio
    submission_dir = os.path.join(ASSIGNMENT_DIR, str(assignment_id), str(submission.userid))
    
    # Obtener el archivo más reciente (podría mejorarse para manejar múltiples archivos)
    files = os.listdir(submission_dir) if os.path.exists(submission_dir) else []
    if not files:
        raise HTTPException(status_code=404, detail="No submission files found")
    
    # Ordenar por fecha de modificación para obtener el más reciente
    files.sort(key=lambda x: os.path.getmtime(os.path.join(submission_dir, x)), reverse=True)
    latest_file = files[0]
    
    return FileResponse(
        path=os.path.join(submission_dir, latest_file),
        filename=f"submission_{submission_id}_{latest_file}"
    )

# Endpoint para subir recursos del curso
@router.post("/resource/{course_id}")
async def upload_resource_file(
    course_id: int,
    user_id: int,
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None)
):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar si el usuario tiene permisos para subir recursos
    user_roles = await prisma.userrole.find_many(
        where={
            "userid": user_id,
            "contextid": course_id  # Asumiendo que contextid representa el curso
        },
        include={"role": True}
    )
    
    # Verificar si el usuario tiene rol de profesor
    is_teacher = False
    for user_role in user_roles:
        if user_role.role.shortname in ["teacher", "editingteacher"]:
            is_teacher = True
            break
    
    if not is_teacher:
        raise HTTPException(status_code=403, detail="Not authorized to upload resources")
    
    # Crear un nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Crear directorio para el recurso si no existe
    resource_course_dir = os.path.join(RESOURCE_DIR, str(course_id))
    if not os.path.exists(resource_course_dir):
        os.makedirs(resource_course_dir)
    
    # Guardar el archivo
    file_path = os.path.join(resource_course_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Crear el recurso en la base de datos
    now = datetime.utcnow()
    new_resource = await prisma.resource.create(data={
        "course": course_id,
        "name": name,
        "intro": description,
        "introformat": 1,  # Formato básico
        "timemodified": now
    })
    
    return {
        "resource_id": new_resource.id,
        "filename": file.filename,
        "stored_filename": unique_filename,
        "message": "Resource uploaded successfully"
    }

# Endpoint para descargar recursos del curso
@router.get("/resource/{resource_id}")
async def download_resource_file(resource_id: int):
    # Verificar si el recurso existe
    resource = await prisma.resource.find_unique(where={"id": resource_id})
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Buscar el archivo en el directorio
    resource_dir = os.path.join(RESOURCE_DIR, str(resource.course))
    
    # En un sistema real, habría una tabla que asocia recursos con sus archivos
    # Aquí, simplemente buscamos el archivo más reciente
    files = os.listdir(resource_dir) if os.path.exists(resource_dir) else []
    if not files:
        raise HTTPException(status_code=404, detail="No resource files found")
    
    # Ordenar por fecha de modificación para obtener el más reciente
    files.sort(key=lambda x: os.path.getmtime(os.path.join(resource_dir, x)), reverse=True)
    latest_file = files[0]
    
    return FileResponse(
        path=os.path.join(resource_dir, latest_file),
        filename=f"resource_{resource_id}_{latest_file}"
    )

# Endpoint para subir imagen de perfil
@router.post("/profile/{user_id}")
async def upload_profile_image(
    user_id: int,
    file: UploadFile = File(...)
):
    # Verificar que es una imagen
    valid_image_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in valid_image_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Crear un nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"profile_{user_id}{file_extension}"
    
    # Guardar el archivo
    user_profile_dir = os.path.join(PROFILE_DIR, str(user_id))
    if not os.path.exists(user_profile_dir):
        os.makedirs(user_profile_dir)
    
    file_path = os.path.join(user_profile_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": unique_filename,
        "message": "Profile image uploaded successfully"
    }

# Endpoint para obtener imagen de perfil
@router.get("/profile/{user_id}")
async def get_profile_image(user_id: int):
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Buscar archivo de perfil del usuario
    user_profile_dir = os.path.join(PROFILE_DIR, str(user_id))
    
    if not os.path.exists(user_profile_dir):
        raise HTTPException(status_code=404, detail="Profile image not found")
    
    # Buscar la imagen de perfil
    profile_files = [f for f in os.listdir(user_profile_dir) if f.startswith("profile_")]
    
    if not profile_files:
        raise HTTPException(status_code=404, detail="Profile image not found")
    
    # Devolver la imagen más reciente
    profile_files.sort(key=lambda x: os.path.getmtime(os.path.join(user_profile_dir, x)), reverse=True)
    latest_profile = profile_files[0]
    
    return FileResponse(path=os.path.join(user_profile_dir, latest_profile))
