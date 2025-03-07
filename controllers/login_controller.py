from fastapi import APIRouter, HTTPException, status
from prisma import Prisma
from pydantic import BaseModel
from bcrypt import checkpw

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

prisma = Prisma()

# Router para login
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

# Endpoint para login
@router.post("", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    await prisma.connect()
    
    # Buscar usuario por nombre de usuario
    user = await prisma.user.find_first(
        where={
            "username": login_data.username
        }
    )
    
    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not checkpw(login_data.password.encode('utf-8'), user.password.encode('utf-8')):
        await prisma.disconnect()
        return LoginResponse(
            success=False,
            message="Credenciales incorrectas"
        )
    
    # Obtener roles del usuario
    user_roles = await prisma.userrole.find_many(
        where={"userid": user.id},
        include={"role": True}
    )
    
    roles = [{"id": ur.role.id, "name": ur.role.name, "shortname": ur.role.shortname} for ur in user_roles]
    
    await prisma.disconnect()
    
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