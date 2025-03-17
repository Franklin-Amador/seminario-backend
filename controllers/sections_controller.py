
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import SectionBase, SectionResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

        
@router.get("/sections", response_model=List[SectionResponse])
async def get_sections():
    sections = await prisma.coursesection.find_many()
    return sections
        
@router.get("/sections/{course_id}", response_model=SectionResponse)
async def get_section_modules(course_id:int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las secciones del curso
    sections = await prisma.coursesection.find_many(where={"course": course_id})
    
    return sections

@router.post("/sections", response_model=SectionResponse)
async def create_section(section: SectionBase):
    try:
        # Contar cuántas secciones tiene el curso
        section_count = await prisma.coursesection.count(where={"course": section.course})
        
        # Asignar el número de sección automáticamente
        new_section_number = section_count + 1
        
        timemodified = datetime.utcnow()
        new_section = await prisma.coursesection.create(
            data={
                "course": section.course,
                "name": section.name,
                "section": new_section_number,
                "summary": section.summary,
                "visible": section.visible,
                "timemodified": timemodified
            }
        )
        return new_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating section: {str(e)}"
        )

@router.put("/sections/{section_id}", response_model=SectionResponse)
async def update_section(section_id: int, section: SectionBase):
    try:
        updated_section = await prisma.coursesection.update(
            where={"id": section_id},
            data={
                "name": section.name,
                "summary": section.summary,
                "visible": section.visible,
                "timemodified": datetime.utcnow()
            }
        )
        return updated_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating section: {str(e)}"
        )

@router.delete("/sections/{section_id}", response_model=SectionResponse)
async def delete_section(section_id: int):
    try:
        deleted_section = await prisma.coursesection.delete(
            where={"id": section_id}
        )
        return deleted_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting section: {str(e)}"
        )
