
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import ResourceBase, ResourceResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)


# ----- OPERACIONES CRUD PARA RECURSOS ----- #

@router.post("/courses/{course_id}/resources", response_model=ResourceResponse)
async def create_resource(course_id: int, resource: ResourceBase):
    if resource.course != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID in path does not match course ID in resource data"
        )
    
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": course_id})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear el recurso
        now = datetime.utcnow()
        new_resource = await prisma.resource.create(
            data={
                "course": course_id,
                "name": resource.name,
                "intro": resource.intro,
                "introformat": resource.introformat,
                "tobemigrated": 0,
                "legacyfiles": 0,
                "display": 0,
                "filterfiles": 0,
                "revision": 1,
                "timemodified": now
            }
        )
        
        return new_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating resource: {str(e)}"
        )

@router.get("/courses/{course_id}/resources", response_model=List[ResourceResponse])
async def get_course_resources(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener los recursos
    resources = await prisma.resource.find_many(
        where={"course": course_id}
    )
    
    return resources

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    resource = await prisma.resource.find_unique(
        where={"id": resource_id}
    )
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource: ResourceBase):
    try:
        # Incrementar la revisión
        existing_resource = await prisma.resource.find_unique(
            where={"id": resource_id}
        )
        
        if not existing_resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Actualizar el recurso
        updated_resource = await prisma.resource.update(
            where={"id": resource_id},
            data={
                "name": resource.name,
                "intro": resource.intro,
                "introformat": resource.introformat,
                "revision": existing_resource.revision + 1,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating resource: {str(e)}"
        )

@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
async def delete_resource(resource_id: int):
    try:
        deleted_resource = await prisma.resource.delete(
            where={"id": resource_id}
        )
        
        return deleted_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting resource: {str(e)}"
        )