

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import SubmissionBase, SubmissionResponse

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
        assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": submission.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Marcar la última entrega como no actual
        await prisma.submission.update_many(
            where={
                "assignment": assignment_id,
                "userid": submission.userid
            },
            data={"latest": False}
        )
        
        # Crear la nueva entrega
        now = datetime.utcnow()
        new_submission = await prisma.submission.create(
            data={
                "assignment": assignment_id,
                "userid": submission.userid,
                "status": submission.status,
                "groupid": submission.groupid,
                "attemptnumber": submission.attemptnumber,
                "latest": True,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        return new_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating submission: {str(e)}"
        )

@router.get("/assignments/{assignment_id}/submissions", response_model=List[SubmissionResponse])
async def get_assignment_submissions(assignment_id: int):
    # Verificar si la tarea existe
    assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Obtener las entregas
    submissions = await prisma.submission.find_many(
        where={"assignment": assignment_id}
    )
    
    return submissions

@router.get("/users/{user_id}/submissions", response_model=List[SubmissionResponse])
async def get_user_submissions(user_id: int):
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener las entregas
    submissions = await prisma.submission.find_many(
        where={"userid": user_id}
    )
    
    return submissions

@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
async def update_submission(submission_id: int, submission: SubmissionBase):
    try:
        # Verificar si la entrega existe
        existing_submission = await prisma.submission.find_unique(
            where={"id": submission_id}
        )
        
        if not existing_submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        
        # Actualizar la entrega
        updated_submission = await prisma.submission.update(
            where={"id": submission_id},
            data={
                "status": submission.status,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating submission: {str(e)}"
        )

@router.delete("/submissions/{submission_id}", response_model=SubmissionResponse)
async def delete_submission(submission_id: int):
    try:
        deleted_submission = await prisma.submission.delete(
            where={"id": submission_id}
        )
        
        return deleted_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting submission: {str(e)}"
        )
