from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import SubmissionBase, SubmissionResponse
from db import fetch_data, fetch_one, execute_query

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA ENTREGAS (SUBMISSIONS) ----- #

@router.post("/assignments/{assignment_id}/submissions", response_model=SubmissionResponse)
async def create_submission(assignment_id: int, submission: SubmissionBase):
    if submission.assignment != assignment_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment ID in path does not match assignment ID in submission data"
        )
    
    try:
        # Verificar si la tarea existe
        assignment_query = """
        SELECT id FROM mdl_assign WHERE id = %s
        """
        assignment = fetch_one(assignment_query, (assignment_id,))
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Verificar si el usuario existe
        user_query = """
        SELECT id FROM mdl_user WHERE id = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (submission.userid,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Marcar la última entrega como no actual
        update_submissions_query = """
        UPDATE mdl_assign_submission
        SET latest = FALSE
        WHERE assignment = %s AND userid = %s
        """
        execute_query(update_submissions_query, (assignment_id, submission.userid))
        
        # Crear la nueva entrega
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_assign_submission (
            assignment, userid, status, groupid, attemptnumber,
            latest, timecreated, timemodified
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            assignment_id,
            submission.userid,
            submission.status,
            submission.groupid,
            submission.attemptnumber,
            True,  # latest
            now,
            now
        )
        
        new_submission = fetch_one(insert_query, values)
        
        return new_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating submission: {str(e)}"
        )

@router.get("/assignments/{assignment_id}/submissions", response_model=List[SubmissionResponse])
async def get_assignment_submissions(assignment_id: int):
    try:
        # Verificar si la tarea existe
        assignment_query = """
        SELECT id FROM mdl_assign WHERE id = %s
        """
        assignment = fetch_one(assignment_query, (assignment_id,))
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Obtener las entregas
        query = """
        SELECT * FROM mdl_assign_submission
        WHERE assignment = %s
        ORDER BY userid, attemptnumber DESC
        """
        submissions = fetch_data(query, (assignment_id,))
        
        return submissions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching submissions: {str(e)}"
        )

@router.get("/users/{user_id}/submissions", response_model=List[SubmissionResponse])
async def get_user_submissions(user_id: int):
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
        
        # Obtener las entregas
        query = """
        SELECT * FROM mdl_assign_submission
        WHERE userid = %s
        ORDER BY assignment, attemptnumber DESC
        """
        submissions = fetch_data(query, (user_id,))
        
        return submissions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching submissions: {str(e)}"
        )

@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
async def update_submission(submission_id: int, submission: SubmissionBase):
    try:
        # Verificar si la entrega existe
        check_query = """
        SELECT * FROM mdl_assign_submission
        WHERE id = %s
        """
        existing_submission = fetch_one(check_query, (submission_id,))
        
        if not existing_submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        
        # Actualizar la entrega
        update_query = """
        UPDATE mdl_assign_submission
        SET status = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            submission.status,
            datetime.utcnow(),
            submission_id
        )
        
        updated_submission = fetch_one(update_query, values)
        
        return updated_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating submission: {str(e)}"
        )

@router.delete("/submissions/{submission_id}", response_model=SubmissionResponse)
async def delete_submission(submission_id: int):
    try:
        # Obtener la entrega antes de eliminarla
        get_query = """
        SELECT * FROM mdl_assign_submission
        WHERE id = %s
        """
        submission = fetch_one(get_query, (submission_id,))
        
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        
        # Eliminar la entrega
        delete_query = """
        DELETE FROM mdl_assign_submission
        WHERE id = %s
        """
        execute_query(delete_query, (submission_id,))
        
        return submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting submission: {str(e)}"
        )