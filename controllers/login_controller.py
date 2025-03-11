from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from bcrypt import checkpw
import bcrypt
from fastapi import Body
from db import prisma_client

# Modelo para la solicitud de login
class LoginRequest(BaseModel):
    username: str
    password: str

# Modelo para la respuesta del login
class LoginResponse(BaseModel):
    success: bool
    user_id: int = None
    username: str = None
    firstname: str = None
    lastname: str = None
    email: str = None
    roles: list = None
    message: str = None
    
# Modelo para la respuesta de actualización masiva
class BulkPasswordUpdateResponse(BaseModel):
    success: bool
    count: int = None
    message: str = None

# Modelo para solicitud de actualización masiva
class BulkPasswordUpdateRequest(BaseModel):
    admin_key: str
    new_password: str = "1234"


# Router para login
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

# Endpoint para login
@router.post("", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    
    # Buscar usuario por nombre de usuario
    user = await prisma_client.user.find_first(
        where={
            "username": login_data.username
        }
    )
    
    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not checkpw(login_data.password.encode('utf-8'), user.password.encode('utf-8')):
        await prisma_client.disconnect()
        return LoginResponse(
            success=False,
            message="Credenciales incorrectas"
        )
    
    # Obtener roles del usuario
    user_roles = await prisma_client.userrole.find_many(
        where={"userid": user.id},
        include={"role": True}
    )
    
    roles = [{"id": ur.role.id, "name": ur.role.name, "shortname": ur.role.shortname} for ur in user_roles]
    
    
    # Devolver información del usuario
    return LoginResponse(
        success=True,
        user_id=user.id,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        roles=roles,
        message="Login exitoso"
    )
    
class UpdatePasswordRequest(BaseModel):
    email: str
    new_password: str

@router.put("/update-password", response_model=LoginResponse)
async def update_password(update_data: UpdatePasswordRequest):
    
    # Buscar usuario por email
    user = await prisma_client.user.find_first(
        where={"email": update_data.email}
    )   
    # Verificar si el usuario existe
    if not user:
        await prisma_client.disconnect()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado"
        )
    
    # Actualizar la contraseña del usuario
    hashed_new_password = bcrypt.hashpw(update_data.new_password.encode('utf-8'), bcrypt.gensalt())
    await prisma_client.user.update(
        where={"id": user.id},
        data={"password": hashed_new_password.decode('utf-8')}
    )
    
    return LoginResponse(
        success=True,
        message="Contraseña actualizada exitosamente"
    )


@router.put("/reset-all-passwords", response_model=BulkPasswordUpdateResponse)
async def reset_all_passwords(update_data: BulkPasswordUpdateRequest):
    # Verificar la clave de administrador (esto debería ser más seguro en producción)
    # En un entorno real, deberías usar variables de entorno o un sistema de secretos
    ADMIN_SECRET_KEY = "papi_claude"  # Cambia esto en producción
    
    if update_data.admin_key != ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clave de administrador incorrecta"
        )
    
    await prisma_client.connect()
    
    try:
        # Obtener todos los usuarios
        users = await prisma_client.user.find_many()
        
        # Encriptar la nueva contraseña una sola vez (todos tendrán la misma)
        hashed_password = bcrypt.hashpw(
            update_data.new_password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Contador de usuarios actualizados
        updated_count = 0
        
        # Actualizar cada usuario individualmente
        for user in users:
            await prisma_client.user.update(
                where={"id": user.id},
                data={"password": hashed_password}
            )
            updated_count += 1
        
        return BulkPasswordUpdateResponse(
            success=True,
            count=updated_count,
            message=f"Se actualizaron {updated_count} contraseñas exitosamente"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contraseñas: {str(e)}"
        )
    