from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import GradeBase, GradeResponse, GradeItemResponse
from db import fetch_data, fetch_one, execute_query

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
        grade_item_query = """
        SELECT * FROM mdl_grade_items
        WHERE id = %s AND courseid = %s
        """
        grade_item = fetch_one(grade_item_query, (grade.itemid, course_id))
        
        if not grade_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade item not found in this course"
            )
        
        # Verificar si el usuario existe
        user_query = """
        SELECT id FROM mdl_user
        WHERE id = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (grade.userid,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una calificación para este usuario y elemento
        existing_grade_query = """
        SELECT id FROM mdl_grade_grades
        WHERE itemid = %s AND userid = %s
        """
        existing_grade = fetch_one(existing_grade_query, (grade.itemid, grade.userid))
        
        now = datetime.utcnow()
        
        if existing_grade:
            # Actualizar la calificación existente
            update_query = """
            UPDATE mdl_grade_grades
            SET rawgrade = %s,
                finalgrade = %s,
                feedback = %s,
                timemodified = %s
            WHERE id = %s
            RETURNING *
            """
            
            values = (
                grade.rawgrade,
                grade.finalgrade,
                grade.feedback,
                now,
                existing_grade['id']
            )
            
            updated_grade = fetch_one(update_query, values)
            return updated_grade
        else:
            # Crear una nueva calificación
            insert_query = """
            INSERT INTO mdl_grade_grades (
                itemid, userid, rawgrade, rawgrademax, rawgrademin,
                finalgrade, feedback, feedbackformat, timecreated, timemodified
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """
            
            values = (
                grade.itemid,
                grade.userid,
                grade.rawgrade,
                grade_item['grademax'],
                grade_item['grademin'],
                grade.finalgrade,
                grade.feedback,
                0,  # feedbackformat
                now,
                now
            )
            
            new_grade = fetch_one(insert_query, values)
            return new_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating grade: {str(e)}"
        )

@router.get("/courses/{course_id}/grades", response_model=List[GradeItemResponse])
async def get_course_grade_items(course_id: int):
    try:
        # Verificar si el curso existe
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Obtener los ítems de calificación del curso
        query = """
        SELECT * FROM mdl_grade_items
        WHERE courseid = %s
        ORDER BY id
        """
        grade_items = fetch_data(query, (course_id,))
        
        return grade_items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching grade items: {str(e)}"
        )

@router.get("/courses/{course_id}/user/{user_id}/grades", response_model=List[GradeResponse])
async def get_user_course_grades(course_id: int, user_id: int):
    try:
        # Verificar si el curso existe
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verificar si el usuario existe
        user_query = """
        SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (user_id,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Obtener los ítems de calificación del curso
        grade_items_query = """
        SELECT id FROM mdl_grade_items
        WHERE courseid = %s
        """
        grade_items = fetch_data(grade_items_query, (course_id,))
        
        if not grade_items:
            return []
        
        # Obtener todas las calificaciones del usuario para los ítems del curso
        item_ids = [item['id'] for item in grade_items]
        placeholders = ','.join(['%s'] * len(item_ids))
        
        query = f"""
        SELECT * FROM mdl_grade_grades
        WHERE itemid IN ({placeholders}) AND userid = %s
        ORDER BY itemid
        """
        
        # Agregar el userid al final de los parámetros
        params = item_ids + [user_id]
        
        grades = fetch_data(query, tuple(params))
        
        return grades
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching grades: {str(e)}"
        )

@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(grade_id: int, grade: GradeBase):
    try:
        # Verificar si la calificación existe
        check_query = """
        SELECT id FROM mdl_grade_grades WHERE id = %s
        """
        existing_grade = fetch_one(check_query, (grade_id,))
        
        if not existing_grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade not found"
            )
        
        # Actualizar la calificación
        update_query = """
        UPDATE mdl_grade_grades
        SET rawgrade = %s,
            finalgrade = %s,
            feedback = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            grade.rawgrade,
            grade.finalgrade,
            grade.feedback,
            datetime.utcnow(),
            grade_id
        )
        
        updated_grade = fetch_one(update_query, values)
        
        return updated_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating grade: {str(e)}"
        )

@router.delete("/grades/{grade_id}", response_model=GradeResponse)
async def delete_grade(grade_id: int):
    try:
        # Obtener la calificación antes de eliminarla
        get_query = """
        SELECT * FROM mdl_grade_grades WHERE id = %s
        """
        grade = fetch_one(get_query, (grade_id,))
        
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade not found"
            )
        
        # Eliminar la calificación
        delete_query = """
        DELETE FROM mdl_grade_grades WHERE id = %s
        """
        execute_query(delete_query, (grade_id,))
        
        return grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting grade: {str(e)}"
        )