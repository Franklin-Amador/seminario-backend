

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import GradeBase, GradeResponse, GradeItemResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA CALIFICACIONES ----- #

@router.post("/courses/{course_id}/grades", response_model=GradeResponse)
async def create_grade(course_id: int, grade: GradeBase):
    try:
        # Verificar si el ítem de calificación existe y pertenece al curso
        grade_item = await prisma.gradeitem.find_unique(where={"id": grade.itemid})
        if not grade_item or grade_item.courseid != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade item not found in this course"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": grade.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una calificación para este usuario y elemento
        existing_grade = await prisma.grade.find_first(
            where={
                "itemid": grade.itemid,
                "userid": grade.userid
            }
        )
        
        now = datetime.utcnow()
        
        if existing_grade:
            # Actualizar la calificación existente
            updated_grade = await prisma.grade.update(
                where={"id": existing_grade.id},
                data={
                    "rawgrade": grade.rawgrade,
                    "finalgrade": grade.finalgrade,
                    "feedback": grade.feedback,
                    "timemodified": now
                }
            )
            return updated_grade
        else:
            # Crear una nueva calificación
            new_grade = await prisma.grade.create(
                data={
                    "itemid": grade.itemid,
                    "userid": grade.userid,
                    "rawgrade": grade.rawgrade,
                    "rawgrademax": grade_item.grademax,
                    "rawgrademin": grade_item.grademin,
                    "finalgrade": grade.finalgrade,
                    "feedback": grade.feedback,
                    "feedbackformat": 0,
                    "timecreated": now,
                    "timemodified": now
                }
            )
            return new_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating grade: {str(e)}"
        )

@router.get("/courses/{course_id}/grades", response_model=List[GradeItemResponse])
async def get_course_grade_items(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener los ítems de calificación del curso
    grade_items = await prisma.gradeitem.find_many(where={"courseid": course_id})
    
    return grade_items

@router.get("/courses/{course_id}/user/{user_id}/grades", response_model=List[GradeResponse])
async def get_user_course_grades(course_id: int, user_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener los ítems de calificación del curso
    grade_items = await prisma.gradeitem.find_many(where={"courseid": course_id})
    
    if not grade_items:
        return []
    
    # Obtener todas las calificaciones del usuario para los ítems del curso
    item_ids = [item.id for item in grade_items]
    grades = await prisma.grade.find_many(
        where={
            "itemid": {
                "in": item_ids
            },
            "userid": user_id
        }
    )
    
    return grades

@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(grade_id: int, grade: GradeBase):
    try:
        # Verificar si la calificación existe
        existing_grade = await prisma.grade.find_unique(
            where={"id": grade_id}
        )
        
        if not existing_grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade not found"
            )
        
        # Actualizar la calificación
        updated_grade = await prisma.grade.update(
            where={"id": grade_id},
            data={
                "rawgrade": grade.rawgrade,
                "finalgrade": grade.finalgrade,
                "feedback": grade.feedback,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating grade: {str(e)}"
        )

@router.delete("/grades/{grade_id}", response_model=GradeResponse)
async def delete_grade(grade_id: int):
    try:
        deleted_grade = await prisma.grade.delete(
            where={"id": grade_id}
        )
        
        return deleted_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting grade: {str(e)}"
        )
        
