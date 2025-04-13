from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import UserBase, UserResponse
from db import fetch_data, fetch_one, execute_query, execute_query_returning_id
from utils import hash_password

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
        query = """
        SELECT id FROM mdl_user 
        WHERE username = %s OR email = %s
        """
        existing_user = fetch_one(query, (user.username, user.email))
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
        # Encriptar la contraseña
        hashed_password = hash_password(user.password)
        
        # Crear el nuevo usuario
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_user (
            username, password, firstname, lastname, email, 
            institution, department, auth, confirmed, lang, 
            timezone, deleted, suspended, mnethostid, 
            timecreated, timemodified
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, username, password, firstname, lastname, email, 
                  institution, department, auth, confirmed, lang, 
                  timezone, deleted, suspended, mnethostid, 
                  timecreated, timemodified
        """
        
        values = (
            user.username, hashed_password, user.firstname, user.lastname, user.email,
            user.institution, user.department, "manual", False, "es",
            "99", False, False, 1,
            now, now
        )
        
        new_user = fetch_one(insert_query, values)
        
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_users(search: Optional[str] = None):
    try:
        # Construir la consulta según si hay término de búsqueda o no
        if search:
            query = """
            SELECT * FROM mdl_user
            WHERE (username ILIKE %s OR firstname ILIKE %s OR lastname ILIKE %s OR email ILIKE %s)
            AND deleted = FALSE
            ORDER BY id
            """
            search_term = f"%{search}%"
            users = fetch_data(query, (search_term, search_term, search_term, search_term))
        else:
            query = """
            SELECT * FROM mdl_user
            WHERE deleted = FALSE
            ORDER BY id
            """
            users = fetch_data(query)
        
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    query = """
    SELECT * FROM mdl_user
    WHERE id = %s AND deleted = FALSE
    """
    user = fetch_one(query, (user_id,))
    
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
        check_query = """
        SELECT id FROM mdl_user
        WHERE id = %s AND deleted = FALSE
        """
        existing_user = fetch_one(check_query, (user_id,))
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Encriptar la contraseña si se proporcionó una nueva
        hashed_password = hash_password(user.password) if user.password else None
        
        # Actualizar el usuario
        update_query = """
        UPDATE mdl_user
        SET username = %s,
            firstname = %s,
            lastname = %s,
            email = %s,
            institution = %s,
            department = %s,
            timemodified = %s
        """
        
        values = [
            user.username,
            user.firstname,
            user.lastname,
            user.email,
            user.institution,
            user.department,
            datetime.utcnow()
        ]
        
        # Agregar la contraseña a la actualización si se proporcionó
        if hashed_password:
            update_query += ", password = %s"
            values.append(hashed_password)
        
        # Completar la consulta y agregar la condición WHERE
        update_query += " WHERE id = %s RETURNING *"
        values.append(user_id)
        
        updated_user = fetch_one(update_query, tuple(values))
        
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
        query = """
        UPDATE mdl_user
        SET deleted = TRUE, timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        deleted_user = fetch_one(query, (datetime.utcnow(), user_id))
        
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return deleted_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting user: {str(e)}"
        )