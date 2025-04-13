from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import RoleBase, RoleResponse
from db import fetch_data, fetch_one, execute_query

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA ROLES ----- #

@router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleBase):
    try:
        # Verificar si ya existe un rol con el mismo shortname
        check_query = """
        SELECT id FROM mdl_role
        WHERE shortname = %s
        """
        existing_role = fetch_one(check_query, (role.shortname,))
        
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this shortname already exists"
            )
        
        # Crear el nuevo rol
        insert_query = """
        INSERT INTO mdl_role (
            name, shortname, description, sortorder, archetype
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            role.name,
            role.shortname,
            role.description,
            role.sortorder,
            role.archetype
        )
        
        new_role = fetch_one(insert_query, values)
        
        return new_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating role: {str(e)}"
        )

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles():
    try:
        query = """
        SELECT * FROM mdl_role
        ORDER BY sortorder
        """
        roles = fetch_data(query)
        
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching roles: {str(e)}"
        )

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int):
    query = """
    SELECT * FROM mdl_role
    WHERE id = %s
    """
    role = fetch_one(query, (role_id,))
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleBase):
    try:
        # Verificar si existe otro rol con el mismo shortname
        check_query = """
        SELECT id FROM mdl_role
        WHERE shortname = %s AND id != %s
        """
        existing_role = fetch_one(check_query, (role.shortname, role_id))
        
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another role with this shortname already exists"
            )
        
        # Actualizar el rol
        update_query = """
        UPDATE mdl_role
        SET name = %s,
            shortname = %s,
            description = %s,
            sortorder = %s,
            archetype = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            role.name,
            role.shortname,
            role.description,
            role.sortorder,
            role.archetype,
            role_id
        )
        
        updated_role = fetch_one(update_query, values)
        
        if not updated_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        return updated_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating role: {str(e)}"
        )

@router.delete("/roles/{role_id}", response_model=RoleResponse)
async def delete_role(role_id: int):
    try:
        # Verificar si hay asignaciones de este rol
        check_query = """
        SELECT COUNT(*) as count FROM mdl_role_assignments
        WHERE roleid = %s
        """
        result = fetch_one(check_query, (role_id,))
        
        if result and result.get('count', 0) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete role with existing assignments"
            )
        
        # Obtener el rol antes de eliminarlo
        get_query = """
        SELECT * FROM mdl_role
        WHERE id = %s
        """
        role = fetch_one(get_query, (role_id,))
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Eliminar el rol
        delete_query = """
        DELETE FROM mdl_role
        WHERE id = %s
        """
        execute_query(delete_query, (role_id,))
        
        return role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting role: {str(e)}"
        )