from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import EnrollmentBase, EnrollmentResponse
from db import fetch_data, fetch_one, execute_query

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
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (enrollment.courseid,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verificar si el usuario existe
        user_query = """
        SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (enrollment.userid,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una matrícula
        existing_enrollment_query = """
        SELECT id FROM mdl_user_enrolments
        WHERE userid = %s AND courseid = %s
        """
        existing_enrollment = fetch_one(existing_enrollment_query, (enrollment.userid, enrollment.courseid))
        
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course"
            )
        
        # Crear la matrícula
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_user_enrolments (
            enrolid, userid, courseid, status,
            timestart, timeend, timecreated, timemodified
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            enrollment.enrolid,
            enrollment.userid,
            enrollment.courseid,
            enrollment.status,
            enrollment.timestart,
            enrollment.timeend,
            now,
            now
        )
        
        new_enrollment = fetch_one(insert_query, values)
        
        # Crear registro de inicio de compleción del curso
        completion_query = """
        INSERT INTO mdl_course_completions (
            userid, course, timeenrolled, timestarted
        )
        VALUES (%s, %s, %s, %s)
        """
        
        execute_query(completion_query, (enrollment.userid, enrollment.courseid, now, now))
        
        return new_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating enrollment: {str(e)}"
        )

@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_course_enrollments(course_id: int):
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
        
        # Obtener las matrículas del curso
        query = """
        SELECT * FROM mdl_user_enrolments
        WHERE courseid = %s
        ORDER BY id
        """
        enrollments = fetch_data(query, (course_id,))
        
        return enrollments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching enrollments: {str(e)}"
        )

@router.get("/users/{user_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_user_enrollments(user_id: int):
    try:
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
        
        # Obtener las matrículas del usuario
        query = """
        SELECT * FROM mdl_user_enrolments
        WHERE userid = %s
        ORDER BY id
        """
        enrollments = fetch_data(query, (user_id,))
        
        return enrollments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching enrollments: {str(e)}"
        )

@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentBase):
    try:
        # Verificar si la matrícula existe
        check_query = """
        SELECT id FROM mdl_user_enrolments WHERE id = %s
        """
        existing_enrollment = fetch_one(check_query, (enrollment_id,))
        
        if not existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Actualizar la matrícula
        update_query = """
        UPDATE mdl_user_enrolments
        SET status = %s,
            timestart = %s,
            timeend = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            enrollment.status,
            enrollment.timestart,
            enrollment.timeend,
            datetime.utcnow(),
            enrollment_id
        )
        
        updated_enrollment = fetch_one(update_query, values)
        
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
        get_query = """
        SELECT * FROM mdl_user_enrolments WHERE id = %s
        """
        enrollment = fetch_one(get_query, (enrollment_id,))
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Eliminar registro de compleción del curso
        delete_completion_query = """
        DELETE FROM mdl_course_completions
        WHERE userid = %s AND course = %s
        """
        execute_query(delete_completion_query, (enrollment['userid'], enrollment['courseid']))
        
        # Eliminar la matrícula
        delete_query = """
        DELETE FROM mdl_user_enrolments WHERE id = %s
        """
        execute_query(delete_query, (enrollment_id,))
        
        return enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting enrollment: {str(e)}"
        )