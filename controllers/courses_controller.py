from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import CourseBase, CourseResponse
from db import fetch_data, fetch_one, execute_query, execute_query_returning_id

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA CURSOS ----- #

@router.post("/courses", response_model=CourseResponse)
async def create_course(course: CourseBase):
    try:
        # Verificar si la categoría existe
        category_query = """
        SELECT id FROM mdl_course_categories WHERE id = %s
        """
        category = fetch_one(category_query, (course.category,))
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist"
            )
        
        # Crear el curso
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_course (
            category, sortorder, fullname, shortname, idnumber, 
            summary, format, showgrades, newsitems, startdate,
            enddate, visible, groupmode, timecreated, timemodified
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            course.category, course.sortorder, course.fullname, course.shortname, course.idnumber,
            course.summary, course.format, True, 5, course.startdate,
            course.enddate, course.visible, 0, now, now
        )
        
        new_course = fetch_one(insert_query, values)
        
        # Crear la relación con la categoría
        category_map_query = """
        INSERT INTO mdl_course_category_map (category, course)
        VALUES (%s, %s)
        """
        execute_query(category_map_query, (course.category, new_course['id']))
        
        # Crear sección inicial del curso
        section_query = """
        INSERT INTO mdl_course_sections (
            course, section, name, summary, visible, timemodified
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(section_query, (new_course['id'], 0, "General", "Sección general", True, now))
        
        return new_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating course: {str(e)}"
        )

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
    category: Optional[int] = None,
    visible_only: bool = True
):
    try:
        # Construir condiciones de búsqueda
        conditions = []
        params = []
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if visible_only:
            conditions.append("visible = %s")
            params.append(True)
        
        # Construir la consulta
        query = "SELECT * FROM mdl_course"
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY id"
        
        courses = fetch_data(query, tuple(params) if params else None)
        
        return courses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching courses: {str(e)}"
        )

@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int):
    query = """
    SELECT * FROM mdl_course
    WHERE id = %s
    """
    course = fetch_one(query, (course_id,))
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course: CourseBase):
    try:
        # Verificar si el curso existe
        check_query = """
        SELECT id FROM mdl_course
        WHERE id = %s
        """
        existing_course = fetch_one(check_query, (course_id,))
        
        if not existing_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Actualizar curso
        update_query = """
        UPDATE mdl_course
        SET category = %s,
            sortorder = %s,
            fullname = %s,
            shortname = %s,
            idnumber = %s,
            summary = %s,
            format = %s,
            startdate = %s,
            enddate = %s,
            visible = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            course.category,
            course.sortorder,
            course.fullname,
            course.shortname,
            course.idnumber,
            course.summary,
            course.format,
            course.startdate,
            course.enddate,
            course.visible,
            datetime.utcnow(),
            course_id
        )
        
        updated_course = fetch_one(update_query, values)
        
        return updated_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating course: {str(e)}"
        )

@router.delete("/courses/{course_id}", response_model=CourseResponse)
async def delete_course(course_id: int):
    try:
        # En lugar de eliminar, hacer que el curso no sea visible
        query = """
        UPDATE mdl_course
        SET visible = FALSE, timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        deleted_course = fetch_one(query, (datetime.utcnow(), course_id))
        
        if not deleted_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return deleted_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting course: {str(e)}"
        )