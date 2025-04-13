from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import shutil
from datetime import datetime
import uuid

from db import fetch_one, fetch_data, execute_query

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
    assignment_query = """
    SELECT id, course FROM mdl_assign WHERE id = %s
    """
    assignment = fetch_one(assignment_query, (assignment_id,))
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Verificar si el usuario existe
    user_query = """
    SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
    """
    user = fetch_one(user_query, (user_id,))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Verificar si el usuario está matriculado en el curso
    enrollment_query = """
    SELECT id FROM mdl_user_enrolments
    WHERE userid = %s AND courseid = %s AND status = 0
    """
    enrollment = fetch_one(enrollment_query, (user_id, assignment['course']))
    
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
    
    # Buscar entregas previas
    submission_query = """
    SELECT id, attemptnumber FROM mdl_assign_submission
    WHERE assignment = %s AND userid = %s
    ORDER BY attemptnumber DESC
    LIMIT 1
    """
    existing_submission = fetch_one(submission_query, (assignment_id, user_id))
    
    if existing_submission:
        # Marcar la última entrega como no actual
        update_query = """
        UPDATE mdl_assign_submission
        SET latest = FALSE
        WHERE assignment = %s AND userid = %s
        """
        execute_query(update_query, (assignment_id, user_id))
        
        # Incrementar el número de intento
        attempt_number = existing_submission['attemptnumber'] + 1
    else:
        attempt_number = 0
    
    # Crear la nueva entrega
    insert_query = """
    INSERT INTO mdl_assign_submission (
        assignment, userid, timecreated, timemodified,
        status, groupid, attemptnumber, latest
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    
    values = (
        assignment_id,
        user_id,
        now,
        now,
        "submitted",
        0,  # groupid
        attempt_number,
        True  # latest
    )
    
    new_submission = fetch_one(insert_query, values)
    
    return {
        "filename": file.filename,
        "stored_filename": unique_filename,
        "submission_id": new_submission['id'],
        "message": "File uploaded successfully"
    }

# Endpoint para descargar archivo de tarea
@router.get("/assignment/{assignment_id}/{submission_id}")
async def download_assignment_file(
    assignment_id: int,
    submission_id: int,
    user_id: Optional[int] = None
):
    # Verificar si la entrega existe
    submission_query = """
    SELECT id, assignment, userid FROM mdl_assign_submission
    WHERE id = %s AND assignment = %s
    """
    submission = fetch_one(submission_query, (submission_id, assignment_id))
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Verificar permisos si se proporciona user_id
    if user_id and submission['userid'] != user_id:
        # Verificar si el usuario es un profesor
        assignment_query = """
        SELECT course FROM mdl_assign
        WHERE id = %s
        """
        assignment = fetch_one(assignment_query, (assignment_id,))
        
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        # Obtener roles del usuario en el contexto del curso
        role_query = """
        SELECT r.shortname
        FROM mdl_role_assignments ra
        JOIN mdl_role r ON ra.roleid = r.id
        WHERE ra.userid = %s AND ra.contextid = %s
        """
        roles = fetch_data(role_query, (user_id, assignment['course']))
        
        # Verificar si el usuario tiene rol de profesor
        is_teacher = False
        for role in roles:
            if role['shortname'] in ["teacher", "editingteacher"]:
                is_teacher = True
                break
        
        if not is_teacher:
            raise HTTPException(status_code=403, detail="Not authorized to access this submission")
    
    # Buscar el archivo en el directorio
    submission_dir = os.path.join(ASSIGNMENT_DIR, str(assignment_id), str(submission['userid']))
    
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
    course_query = """
    SELECT id FROM mdl_course WHERE id = %s
    """
    course = fetch_one(course_query, (course_id,))
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verificar si el usuario existe
    user_query = """
    SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
    """
    user = fetch_one(user_query, (user_id,))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar si el usuario tiene permisos para subir recursos
    role_query = """
    SELECT r.shortname
    FROM mdl_role_assignments ra
    JOIN mdl_role r ON ra.roleid = r.id
    WHERE ra.userid = %s AND ra.contextid = %s
    """
    roles = fetch_data(role_query, (user_id, course_id))
    
    # Verificar si el usuario tiene rol de profesor
    is_teacher = False
    for role in roles:
        if role['shortname'] in ["teacher", "editingteacher"]:
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
    insert_query = """
    INSERT INTO mdl_resource (
        course, name, intro, introformat, timemodified
    )
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """
    
    values = (
        course_id,
        name,
        description or "",
        1,  # Formato básico
        now
    )
    
    new_resource = fetch_one(insert_query, values)
    
    return {
        "resource_id": new_resource['id'],
        "filename": file.filename,
        "stored_filename": unique_filename,
        "message": "Resource uploaded successfully"
    }

# Endpoint para descargar recursos del curso
@router.get("/resource/{resource_id}")
async def download_resource_file(resource_id: int):
    # Verificar si el recurso existe
    resource_query = """
    SELECT id, course FROM mdl_resource WHERE id = %s
    """
    resource = fetch_one(resource_query, (resource_id,))
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Buscar el archivo en el directorio
    resource_dir = os.path.join(RESOURCE_DIR, str(resource['course']))
    
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
    user_query = """
    SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
    """
    user = fetch_one(user_query, (user_id,))
    
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
    user_query = """
    SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
    """
    user = fetch_one(user_query, (user_id,))
    
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