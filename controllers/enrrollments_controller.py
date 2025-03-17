
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import EnrollmentBase, EnrollmentResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)


# ----- OPERACIONES CRUD PARA MATRÍCULAS (ENROLLMENTS) ----- #

@router.post("/enrollments", response_model=EnrollmentResponse)
async def create_enrollment(enrollment: EnrollmentBase):
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": enrollment.courseid})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": enrollment.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una matrícula
        existing_enrollment = await prisma.enrollment.find_first(
            where={
                "userid": enrollment.userid,
                "courseid": enrollment.courseid
            }
        )
        
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course"
            )
        
        # Crear la matrícula
        now = datetime.utcnow()
        new_enrollment = await prisma.enrollment.create(
            data={
                "enrolid": enrollment.enrolid,
                "userid": enrollment.userid,
                "courseid": enrollment.courseid,
                "status": enrollment.status,
                "timestart": enrollment.timestart,
                "timeend": enrollment.timeend,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        # Crear registro de inicio de compleción del curso
        await prisma.coursecompletion.create(
            data={
                "userid": enrollment.userid,
                "course": enrollment.courseid,
                "timeenrolled": now,
                "timestarted": now
            }
        )
        
        return new_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating enrollment: {str(e)}"
        )

@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_course_enrollments(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las matrículas del curso
    enrollments = await prisma.enrollment.find_many(where={"courseid": course_id})
    
    return enrollments

@router.get("/users/{user_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_user_enrollments(user_id: int):
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener las matrículas del usuario
    enrollments = await prisma.enrollment.find_many(where={"userid": user_id})
    
    return enrollments

@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentBase):
    try:
        # Verificar si la matrícula existe
        existing_enrollment = await prisma.enrollment.find_unique(
            where={"id": enrollment_id}
        )
        
        if not existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Actualizar la matrícula
        updated_enrollment = await prisma.enrollment.update(
            where={"id": enrollment_id},
            data={
                "status": enrollment.status,
                "timestart": enrollment.timestart,
                "timeend": enrollment.timeend,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating enrollment: {str(e)}"
        )

@router.delete("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def delete_enrollment(enrollment_id: int):
    try:
        # Obtener información de la matrícula
        enrollment = await prisma.enrollment.find_unique(
            where={"id": enrollment_id}
        )
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Eliminar registro de compleción del curso
        await prisma.coursecompletion.delete_many(
            where={
                "userid": enrollment.userid,
                "course": enrollment.courseid
            }
        )
        
        # Eliminar la matrícula
        deleted_enrollment = await prisma.enrollment.delete(
            where={"id": enrollment_id}
        )
        
        return deleted_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting enrollment: {str(e)}"
        )