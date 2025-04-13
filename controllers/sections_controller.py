from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import SectionBase, SectionResponse
from db import fetch_data, fetch_one, execute_query

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

@router.get("/sections", response_model=List[SectionResponse])
async def get_sections():
    try:
        query = """
        SELECT * FROM mdl_course_sections
        ORDER BY course, section
        """
        sections = fetch_data(query)
        
        return sections
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sections: {str(e)}"
        )

@router.get("/sections/{course_id}", response_model=List[SectionResponse])
async def get_section_modules(course_id: int):
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
        
        # Obtener las secciones del curso
        query = """
        SELECT * FROM mdl_course_sections
        WHERE course = %s
        ORDER BY section
        """
        sections = fetch_data(query, (course_id,))
        
        return sections
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sections: {str(e)}"
        )

@router.post("/sections", response_model=SectionResponse)
async def create_section(section: SectionBase):
    try:
        # Verificar si el curso existe
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (section.course,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Contar cuántas secciones tiene el curso para asignar un nuevo número
        count_query = """
        SELECT COUNT(*) as count FROM mdl_course_sections
        WHERE course = %s
        """
        result = fetch_one(count_query, (section.course,))
        
        # Asignar el número de sección automáticamente
        new_section_number = result['count'] + 1 if result else 1
        
        # Crear la nueva sección
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_course_sections (
            course, section, name, summary, visible, timemodified
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            section.course,
            new_section_number,
            section.name,
            section.summary,
            section.visible,
            now
        )
        
        new_section = fetch_one(insert_query, values)
        
        return new_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating section: {str(e)}"
        )

@router.put("/sections/{section_id}", response_model=SectionResponse)
async def update_section(section_id: int, section: SectionBase):
    try:
        # Verificar si la sección existe
        check_query = """
        SELECT id FROM mdl_course_sections
        WHERE id = %s
        """
        existing_section = fetch_one(check_query, (section_id,))
        
        if not existing_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found"
            )
        
        # Actualizar la sección
        update_query = """
        UPDATE mdl_course_sections
        SET name = %s,
            summary = %s,
            visible = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            section.name,
            section.summary,
            section.visible,
            datetime.utcnow(),
            section_id
        )
        
        updated_section = fetch_one(update_query, values)
        
        return updated_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating section: {str(e)}"
        )

@router.delete("/sections/{section_id}", response_model=SectionResponse)
async def delete_section(section_id: int):
    try:
        # Verificar si hay módulos en la sección
        check_query = """
        SELECT COUNT(*) as count FROM mdl_course_modules
        WHERE section = %s
        """
        result = fetch_one(check_query, (section_id,))
        
        if result and result.get('count', 0) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete section with existing modules"
            )
        
        # Obtener la sección antes de eliminarla
        get_query = """
        SELECT * FROM mdl_course_sections
        WHERE id = %s
        """
        section = fetch_one(get_query, (section_id,))
        
        if not section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found"
            )
        
        # Evitar eliminar la sección 0 (general) de un curso
        if section['section'] == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the general section of a course"
            )
        
        # Eliminar la sección
        delete_query = """
        DELETE FROM mdl_course_sections
        WHERE id = %s
        """
        execute_query(delete_query, (section_id,))
        
        return section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting section: {str(e)}"
        )