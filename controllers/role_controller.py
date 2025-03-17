
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import RoleBase, RoleResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA ROLES ----- #

@router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleBase):
    try:
        new_role = await prisma.role.create(
            data={
                "name": role.name,
                "shortname": role.shortname,
                "description": role.description,
                "sortorder": role.sortorder,
                "archetype": role.archetype
            }
        )
        return new_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating role: {str(e)}"
        )

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles():
    roles = await prisma.role.find_many()
    return roles

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int):
    role = await prisma.role.find_unique(where={"id": role_id})
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleBase):
    try:
        updated_role = await prisma.role.update(
            where={"id": role_id},
            data={
                "name": role.name,
                "shortname": role.shortname,
                "description": role.description,
                "sortorder": role.sortorder,
                "archetype": role.archetype
            }
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
        deleted_role = await prisma.role.delete(where={"id": role_id})
        return deleted_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting role: {str(e)}"
        )