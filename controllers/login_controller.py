from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel
from datetime import datetime

from models.base import LoginRequest, LoginResponse, BulkPasswordUpdateRequest, BulkPasswordUpdateResponse
from db import fetch_one, fetch_data, execute_query

# Router para login
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

# Endpoint para login
@router.post("", response_model=LoginResponse)
async def login(login_data: LoginRequest, request: Request):
    try:
        # Buscar usuario por nombre de usuario
        user_query = """
        SELECT id, username, password, firstname, lastname, email
        FROM mdl_user
        WHERE username = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (login_data.username,))
        
        # Verificar si el usuario existe y la contraseña coincide
        # Para esta versión simplificada, no hacemos hashing
        if not user or user['password'] != login_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Obtener roles del usuario (simplificado, sin verificación)
        roles_query = """
        SELECT r.id, r.name, r.shortname
        FROM mdl_role_assignments ra
        JOIN mdl_role r ON ra.roleid = r.id
        WHERE ra.userid = %s
        """
        user_roles = fetch_data(roles_query, (user['id'],))
        
        roles = [{"id": role['id'], "name": role['name'], "shortname": role['shortname']} for role in user_roles]
        
        # Registrar el inicio de sesión (opcional)
        log_query = """
        INSERT INTO login_audit (username, success, timestamp)
        VALUES (%s, %s, %s)
        """
        execute_query(log_query, (login_data.username, True, datetime.utcnow()))
        
        # Devolver información del usuario
        return LoginResponse(
            success=True,
            user_id=user['id'],
            username=user['username'],
            firstname=user['firstname'],
            lastname=user['lastname'],
            email=user['email'],
            roles=roles,
            message="Login exitoso"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el proceso de login: {str(e)}"
        )

class UpdatePasswordRequest(BaseModel):
    email: str
    new_password: str

@router.put("/update-password", response_model=LoginResponse)
async def update_password(update_data: UpdatePasswordRequest):
    try:
        # Buscar usuario por email
        user_query = """
        SELECT id FROM mdl_user
        WHERE email = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (update_data.email,))
        
        # Verificar si el usuario existe
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no encontrado"
            )
        
        # Actualizar la contraseña del usuario (sin hash para simplificar)
        update_query = """
        UPDATE mdl_user
        SET password = %s, timemodified = %s
        WHERE id = %s
        """
        execute_query(update_query, (update_data.new_password, datetime.utcnow(), user['id']))
        
        return LoginResponse(
            success=True,
            message="Contraseña actualizada exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contraseña: {str(e)}"
        )

@router.put("/reset-all-passwords", response_model=BulkPasswordUpdateResponse)
async def reset_all_passwords(update_data: BulkPasswordUpdateRequest):
    # Verificación simplificada
    ADMIN_SECRET_KEY = "papi_claude"
    
    if update_data.admin_key != ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave de administrador incorrecta"
        )
    
    try:
        # Actualizar todas las contraseñas (sin hash)
        update_query = """
        UPDATE mdl_user
        SET password = %s, timemodified = %s
        WHERE deleted = FALSE
        """
        
        # Ejecutar la actualización
        rows_affected = execute_query(update_query, (update_data.new_password, datetime.utcnow()))
        
        return BulkPasswordUpdateResponse(
            success=True,
            count=rows_affected,
            message=f"Se actualizaron {rows_affected} contraseñas exitosamente"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contraseñas: {str(e)}"
        )