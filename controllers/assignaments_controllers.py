
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import bcrypt
from db import prisma_client as prisma

from models.base import AssignmentBase, AssignmentResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)



# ----- OPERACIONES CRUD PARA ASSIGNACIONES ----- #

@router.post("/courses/{course_id}/assignments", response_model=AssignmentResponse)
async def create_assignment(
    course_id: int,
    assignment: AssignmentBase
):
    if assignment.course != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID in path does not match course ID in assignment data"
        )
    
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": course_id})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear la tarea
        now = datetime.utcnow()
        new_assignment = await prisma.assignment.create(
            data={
                "course": course_id,
                "name": assignment.name,
                "intro": assignment.intro,
                "introformat": assignment.introformat,
                "section": assignment.section,
                "duedate": assignment.duedate,
                "allowsubmissionsfromdate": assignment.allowsubmissionsfromdate,
                "grade": assignment.grade,
                "timemodified": now,
                "alwaysshowdescription": True,
                "nosubmissions": False,
                "submissiondrafts": False,
                "sendnotifications": False,
                "sendlatenotifications": False,
                "requiresubmissionstatement": False,
                "completionsubmit": False,
                "teamsubmission": False,
                "requireallteammemberssubmit": False,
                "teamsubmissiongroupingid": 0,
                "blindmarking": False,
                "revealidentities": False,
                "attemptreopenmethod": "none",
                "maxattempts": -1,
                "markingworkflow": False,
                "markingallocation": False
            }
        )
        
        # Crear un ítem de calificación para la tarea
        if assignment.grade:
            await prisma.gradeitem.create(
                data={
                    "courseid": course_id,
                    "itemname": assignment.name,
                    "itemtype": "mod",
                    "itemmodule": "assign",
                    "iteminstance": new_assignment.id,
                    "grademax": assignment.grade,
                    "grademin": 0,
                    "timecreated": now,
                    "timemodified": now
                }
            )
        
        return new_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating assignment: {str(e)}"
        )

@router.get("/courses/{course_id}/assignments", response_model=List[AssignmentResponse])
async def get_course_assignments(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las tareas del curso
    assignments = await prisma.assignment.find_many(where={"course": course_id})
    
    return assignments

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int):
    assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return assignment

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(assignment_id: int, assignment: AssignmentBase):
    try:
        updated_assignment = await prisma.assignment.update(
            where={"id": assignment_id},
            data={
                "section": assignment.section,
                "name": assignment.name,
                "intro": assignment.intro,
                "introformat": assignment.introformat,
                "duedate": assignment.duedate,
                "allowsubmissionsfromdate": assignment.allowsubmissionsfromdate,
                "grade": assignment.grade,
                "timemodified": datetime.utcnow()
            }
        )
        
        # Actualizar el ítem de calificación si existe
        if assignment.grade:
            grade_item = await prisma.gradeitem.find_first(
                where={
                    "itemmodule": "assign",
                    "iteminstance": assignment_id
                }
            )
            
            if grade_item:
                await prisma.gradeitem.update(
                    where={"id": grade_item.id},
                    data={
                        "itemname": assignment.name,
                        "grademax": assignment.grade,
                        "timemodified": datetime.utcnow()
                    }
                )
        
        return updated_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating assignment: {str(e)}"
        )

@router.delete("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def delete_assignment(assignment_id: int):
    try:
        # Eliminar las entregas asociadas
        await prisma.submission.delete_many(
            where={"assignment": assignment_id}
        )
        
        # Eliminar el ítem de calificación si existe
        grade_item = await prisma.gradeitem.find_first(
            where={
                "itemmodule": "assign",
                "iteminstance": assignment_id
            }
        )
        
        if grade_item:
            await prisma.gradeitem.delete(
                where={"id": grade_item.id}
            )
        
        # Eliminar la tarea
        deleted_assignment = await prisma.assignment.delete(
            where={"id": assignment_id}
        )
        
        return deleted_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting assignment: {str(e)}"
        )