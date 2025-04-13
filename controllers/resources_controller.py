from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import ResourceBase, ResourceResponse
from db import fetch_data, fetch_one, execute_query

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
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear el recurso
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_resource (
            course, name, intro, introformat, tobemigrated,
            legacyfiles, display, filterfiles, revision, timemodified
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            course_id,
            resource.name,
            resource.intro,
            resource.introformat,
            0,  # tobemigrated
            0,  # legacyfiles
            0,  # display
            0,  # filterfiles
            1,  # revision
            now  # timemodified
        )
        
        new_resource = fetch_one(insert_query, values)
        
        return new_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating resource: {str(e)}"
        )

@router.get("/courses/{course_id}/resources", response_model=List[ResourceResponse])
async def get_course_resources(course_id: int):
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
        
        # Obtener los recursos
        query = """
        SELECT * FROM mdl_resource
        WHERE course = %s
        ORDER BY id
        """
        resources = fetch_data(query, (course_id,))
        
        return resources
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching resources: {str(e)}"
        )

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    query = """
    SELECT * FROM mdl_resource
    WHERE id = %s
    """
    resource = fetch_one(query, (resource_id,))
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource: ResourceBase):
    try:
        # Obtener el recurso existente para incrementar la revisión
        get_query = """
        SELECT revision FROM mdl_resource
        WHERE id = %s
        """
        existing_resource = fetch_one(get_query, (resource_id,))
        
        if not existing_resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Actualizar el recurso
        update_query = """
        UPDATE mdl_resource
        SET name = %s,
            intro = %s,
            introformat = %s,
            revision = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            resource.name,
            resource.intro,
            resource.introformat,
            existing_resource['revision'] + 1,  # Incrementar la revisión
            datetime.utcnow(),
            resource_id
        )
        
        updated_resource = fetch_one(update_query, values)
        
        return updated_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating resource: {str(e)}"
        )

@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
async def delete_resource(resource_id: int):
    try:
        # Obtener el recurso antes de eliminarlo
        get_query = """
        SELECT * FROM mdl_resource
        WHERE id = %s
        """
        resource = fetch_one(get_query, (resource_id,))
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Eliminar el recurso
        delete_query = """
        DELETE FROM mdl_resource
        WHERE id = %s
        """
        execute_query(delete_query, (resource_id,))
        
        return resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting resource: {str(e)}"
        )