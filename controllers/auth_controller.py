from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prisma import Prisma
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Esquema para el modelo de token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Esquema para el usuario durante la autenticación
class UserAuth(BaseModel):
    username: str
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None

# Configuración de seguridad
SECRET_KEY = "REEMPLAZAR_CON_UNA_CLAVE_SECRETA_SEGURA"  # En producción, usar una clave secreta real
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

prisma = Prisma()

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para hashear la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Función para autenticar usuario
async def authenticate_user(username: str, password: str):
    await prisma.connect()
    user = await prisma.user.find_unique(where={"username": username})
    await prisma.disconnect()
    
    if not user:
        return False
    # En un entorno real, deberías verificar el hash de la contraseña
    # Por simplicidad, comparamos directamente, pero esto NO es seguro para producción
    if not verify_password(password, user.password):
        return False
    return user

# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    await prisma.connect()
    user = await prisma.user.find_unique(where={"username": token_data.username})
    await prisma.disconnect()
    
    if user is None:
        raise credentials_exception
    return user

# Función para obtener el usuario actual activo
async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.deleted or current_user.suspended:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Router para autenticación
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Not authorized"}}
)

# Endpoint para obtener token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para obtener información del usuario actual
@router.get("/me", response_model=UserAuth)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return UserAuth(
        username=current_user.username,
        email=current_user.email,
        firstname=current_user.firstname,
        lastname=current_user.lastname
    )