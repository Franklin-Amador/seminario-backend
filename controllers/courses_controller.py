

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import CourseBase, CourseResponse

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
        category = await prisma.category.find_unique(where={"id": course.category})
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist"
            )
        
        # Crear el curso
        now = datetime.utcnow()
        new_course = await prisma.course.create(
            data={
                "category": course.category,
                "sortorder": course.sortorder,
                "fullname": course.fullname,
                "shortname": course.shortname,
                "idnumber": course.idnumber,
                "summary": course.summary,
                "format": course.format,
                "showgrades": True,
                "newsitems": 5,
                "startdate": course.startdate,
                "enddate": course.enddate,
                "visible": course.visible,
                "groupmode": 0,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        # Crear la relación con la categoría
        await prisma.categorycourse.create(
            data={
                "categoryId": course.category,
                "courseId": new_course.id
            }
        )
        
        # Crear sección inicial del curso
        await prisma.coursesection.create(
            data={
                "course": new_course.id,
                "section": 0,
                "name": "General",
                "summary": "Sección general",
                "visible": True,
                "timemodified": now
            }
        )
        
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
    # Construir condiciones de búsqueda
    where_conditions = {}
    if category:
        where_conditions["category"] = category
    if visible_only:
        where_conditions["visible"] = True
    
    courses = await prisma.course.find_many(where=where_conditions)
    
    return courses

@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int):
    course = await prisma.course.find_unique(where={"id": course_id})
    
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
        existing_course = await prisma.course.find_unique(where={"id": course_id})
        if not existing_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Actualizar curso
        updated_course = await prisma.course.update(
            where={"id": course_id},
            data={
                "category": course.category,
                "sortorder": course.sortorder,
                "fullname": course.fullname,
                "shortname": course.shortname,
                "idnumber": course.idnumber,
                "summary": course.summary,
                "format": course.format,
                "startdate": course.startdate,
                "enddate": course.enddate,
                "visible": course.visible,
                "timemodified": datetime.utcnow()
            }
        )
        
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
        deleted_course = await prisma.course.update(
            where={"id": course_id},
            data={
                "visible": False,
                "timemodified": datetime.utcnow()
            }
        )
        
        return deleted_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting course: {str(e)}"
        )