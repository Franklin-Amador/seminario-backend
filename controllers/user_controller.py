
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import bcrypt
from db import prisma_client as prisma

from models.base import UserBase, UserResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA USUARIOS ----- #

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserBase):
    try:
        # Verificar si el nombre de usuario o email ya existen
        existing_user = await prisma.user.find_first(
            where={
                "OR": [
                    {"username": user.username},
                    {"email": user.email}
                ]
            }
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
         # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Crear el nuevo usuario
        now = datetime.utcnow()
        new_user = await prisma.user.create(
            data={
                "username": user.username,
                "password": hashed_password,  # En producción, esto debería estar hasheado
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "institution": user.institution,
                "department": user.department,
                "auth": "manual",
                "confirmed": False,
                "lang": "es",
                "timezone": "99",
                "deleted": False,
                "suspended": False,
                "mnethostid": 1,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_users(search: Optional[str] = None):
    # Buscar usuarios
    if search:
        users = await prisma.user.find_many(
            where={
                "OR": [
                    {"username": {"contains": search}},
                    {"firstname": {"contains": search}},
                    {"lastname": {"contains": search}},
                    {"email": {"contains": search}}
                ]
            }
        )
    else:
        users = await prisma.user.find_many()
    
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserBase):
    try:
        # Verificar si el usuario existe
        existing_user = await prisma.user.find_unique(where={"id": user_id})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Actualizar usuario
        updated_user = await prisma.user.update(
            where={"id": user_id},
            data={
                "username": user.username,
                "password": user.password,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "institution": user.institution,
                "department": user.department,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    try:
        # En lugar de eliminar físicamente, marcamos como eliminado
        deleted_user = await prisma.user.update(
            where={"id": user_id},
            data={
                "deleted": True,
                "timemodified": datetime.utcnow()
            }
        )
        
        return deleted_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting user: {str(e)}"
        )