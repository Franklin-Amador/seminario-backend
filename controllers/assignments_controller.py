from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import AssignmentBase, AssignmentResponse
from db import fetch_data, fetch_one, execute_query, execute_query_returning_id

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
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear la tarea
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_assign (
            course, name, intro, introformat, section,
            duedate, allowsubmissionsfromdate, grade, timemodified,
            alwaysshowdescription, nosubmissions, submissiondrafts,
            sendnotifications, sendlatenotifications, requiresubmissionstatement,
            completionsubmit, teamsubmission, requireallteammemberssubmit,
            teamsubmissiongroupingid, blindmarking, revealidentities,
            attemptreopenmethod, maxattempts, markingworkflow, markingallocation
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            course_id,
            assignment.name,
            assignment.intro,
            assignment.introformat,
            assignment.section,
            assignment.duedate,
            assignment.allowsubmissionsfromdate,
            assignment.grade,
            now,
            True,  # alwaysshowdescription
            False,  # nosubmissions
            False,  # submissiondrafts
            False,  # sendnotifications
            False,  # sendlatenotifications
            False,  # requiresubmissionstatement
            False,  # completionsubmit
            False,  # teamsubmission
            False,  # requireallteammemberssubmit
            0,     # teamsubmissiongroupingid
            False,  # blindmarking
            False,  # revealidentities
            "none",  # attemptreopenmethod
            -1,     # maxattempts
            False,  # markingworkflow
            False   # markingallocation
        )
        
        new_assignment = fetch_one(insert_query, values)
        
        # Crear un ítem de calificación para la tarea si se especificó una nota
        if assignment.grade:
            grade_item_query = """
            INSERT INTO mdl_grade_items (
                courseid, itemname, itemtype, itemmodule, iteminstance,
                grademax, grademin, timecreated, timemodified
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            grade_item_values = (
                course_id,
                assignment.name,
                "mod",
                "assign",
                new_assignment['id'],
                assignment.grade,
                0,  # grademin
                now,
                now
            )
            
            execute_query(grade_item_query, grade_item_values)
        
        return new_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating assignment: {str(e)}"
        )

@router.get("/courses/{course_id}/assignments", response_model=List[AssignmentResponse])
async def get_course_assignments(course_id: int):
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
        
        # Obtener las tareas del curso
        query = """
        SELECT * FROM mdl_assign
        WHERE course = %s
        ORDER BY id
        """
        assignments = fetch_data(query, (course_id,))
        
        return assignments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching assignments: {str(e)}"
        )

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int):
    query = """
    SELECT * FROM mdl_assign
    WHERE id = %s
    """
    assignment = fetch_one(query, (assignment_id,))
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return assignment

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(assignment_id: int, assignment: AssignmentBase):
    try:
        # Actualizar la tarea
        update_query = """
        UPDATE mdl_assign
        SET section = %s,
            name = %s,
            intro = %s,
            introformat = %s,
            duedate = %s,
            allowsubmissionsfromdate = %s,
            grade = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            assignment.section,
            assignment.name,
            assignment.intro,
            assignment.introformat,
            assignment.duedate,
            assignment.allowsubmissionsfromdate,
            assignment.grade,
            datetime.utcnow(),
            assignment_id
        )
        
        updated_assignment = fetch_one(update_query, values)
        
        if not updated_assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Actualizar el ítem de calificación si existe y se especificó una nota
        if assignment.grade:
            grade_item_query = """
            SELECT id FROM mdl_grade_items
            WHERE itemmodule = 'assign' AND iteminstance = %s
            """
            grade_item = fetch_one(grade_item_query, (assignment_id,))
            
            if grade_item:
                update_grade_item_query = """
                UPDATE mdl_grade_items
                SET itemname = %s,
                    grademax = %s,
                    timemodified = %s
                WHERE id = %s
                """
                
                execute_query(
                    update_grade_item_query,
                    (assignment.name, assignment.grade, datetime.utcnow(), grade_item['id'])
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
        # Obtener la tarea antes de eliminarla
        get_query = """
        SELECT * FROM mdl_assign
        WHERE id = %s
        """
        assignment = fetch_one(get_query, (assignment_id,))
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Eliminar las entregas asociadas
        delete_submissions_query = """
        DELETE FROM mdl_assign_submission
        WHERE assignment = %s
        """
        execute_query(delete_submissions_query, (assignment_id,))
        
        # Eliminar el ítem de calificación si existe
        grade_item_query = """
        SELECT id FROM mdl_grade_items
        WHERE itemmodule = 'assign' AND iteminstance = %s
        """
        grade_item = fetch_one(grade_item_query, (assignment_id,))
        
        if grade_item:
            delete_grade_item_query = """
            DELETE FROM mdl_grade_items
            WHERE id = %s
            """
            execute_query(delete_grade_item_query, (grade_item['id'],))
        
        # Eliminar la tarea
        delete_query = """
        DELETE FROM mdl_assign
        WHERE id = %s
        """
        execute_query(delete_query, (assignment_id,))
        
        return assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting assignment: {str(e)}"
        )