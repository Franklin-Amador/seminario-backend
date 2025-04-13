from fastapi import APIRouter, HTTPException, status, Request, Depends
from pydantic import BaseModel, Field, ValidationError
import bcrypt
from typing import Optional, List, Dict, Any
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear pool de conexiones para mejor rendimiento
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:root1234@localhost:5433/campus_virtual")
pool = ThreadedConnectionPool(minconn=5, maxconn=20, dsn=DATABASE_URL)

@contextmanager
def get_db_connection():
    """Context manager para obtener una conexión del pool y devolverla automáticamente."""
    conn = None
    try:
        conn = pool.getconn()
        conn.autocommit = False  # Usamos transacciones explícitas
        yield conn
    except psycopg2.Error as e:
        logger.error(f"Error al obtener conexión de la base de datos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión a la base de datos"
        )
    finally:
        if conn:
            pool.putconn(conn)

# Modelos de datos
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)

class LoginResponse(BaseModel):
    success: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    
class BulkPasswordUpdateResponse(BaseModel):
    success: bool
    count: Optional[int] = None
    message: Optional[str] = None

class BulkPasswordUpdateRequest(BaseModel):
    admin_key: str
    new_password: str = "1234"

class UpdatePasswordRequest(BaseModel):
    email: str
    new_password: str

# Router
router = APIRouter(
    prefix="/login",
    tags=["login"],
)

# Obtener información del cliente para auditoría
def get_client_info(request: Request):
    return {
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent", "")
    }

# Endpoint para login optimizado
# @router.post("", response_model=LoginResponse)
async def login(login_data: LoginRequest, request: Request):
    start_time = time.time()
    client_info = get_client_info(request)
    success = False
    
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # El trabajo real de validación ocurre en Python con bcrypt
                # porque la base de datos no puede manejar esta función específica
                
                # Primero obtenemos el usuario para verificar la contraseña
                cur.execute("""
                    SELECT id, username, password, firstname, lastname, email 
                    FROM mdl_user 
                    WHERE username = %s AND deleted = FALSE
                """, (login_data.username,))
                
                user = cur.fetchone()
                
                # Verificar si el usuario existe y la contraseña es correcta
                if not user or not bcrypt.checkpw(
                    login_data.password.encode('utf-8'), 
                    user["password"].encode('utf-8')
                ):
                    # Registrar intento fallido
                    cur.execute(
                        "SELECT audit_login_attempt(%s, %s, %s, %s)",
                        (login_data.username, client_info["ip"], client_info["user_agent"], False)
                    )
                    conn.commit()
                    
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciales incorrectas"
                    )
                
                # Si llegamos aquí, las credenciales son correctas
                # Obtenemos los roles usando el procedimiento optimizado
                cur.execute("""
                    SELECT r.id, r.name, r.shortname
                    FROM mdl_role_assignments ra
                    JOIN mdl_role r ON ra.roleid = r.id
                    WHERE ra.userid = %s
                """, (user["id"],))
                
                roles = []
                for role in cur.fetchall():
                    roles.append({
                        "id": role["id"],
                        "name": role["name"],
                        "shortname": role["shortname"]
                    })
                
                # Registrar login exitoso
                cur.execute(
                    "SELECT audit_login_attempt(%s, %s, %s, %s)",
                    (login_data.username, client_info["ip"], client_info["user_agent"], True)
                )
                conn.commit()
                
                success = True
                
                # Devolver información del usuario
                return LoginResponse(
                    success=True,
                    user_id=user["id"],
                    username=user["username"],
                    firstname=user["firstname"],
                    lastname=user["lastname"],
                    email=user["email"],
                    roles=roles,
                    message="Login exitoso"
                )
    except HTTPException:
        # Re-lanzar las excepciones HTTP
        raise
    except Exception as e:
        logger.error(f"Error de login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}"
        )
    finally:
        duration = time.time() - start_time
        logger.info(f"Login attempt: user={login_data.username}, success={success}, duration={duration:.3f}s")

# @router.put("/update-password", response_model=LoginResponse)
async def update_password(update_data: UpdatePasswordRequest):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Encriptar la nueva contraseña
                hashed_password = bcrypt.hashpw(
                    update_data.new_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Usar procedimiento almacenado para actualizar contraseña
                cur.execute("SELECT * FROM update_user_password(%s, %s)",
                           (update_data.email, hashed_password))
                
                result = cur.fetchone()
                conn.commit()
                
                if not result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result["message"]
                    )
                
                return LoginResponse(
                    success=True,
                    user_id=result["user_id"],
                    message=result["message"]
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar contraseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la contraseña: {str(e)}"
        )

# @router.put("/reset-all-passwords", response_model=BulkPasswordUpdateResponse)
async def reset_all_passwords(update_data: BulkPasswordUpdateRequest):
    try:
        # Clave de administrador (debe moverse a variables de entorno en producción)
        ADMIN_SECRET_KEY = "papi_claude"
        
        if update_data.admin_key != ADMIN_SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Clave de administrador incorrecta"
            )
        
        with get_db_connection() as conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Encriptar la nueva contraseña
                    hashed_password = bcrypt.hashpw(
                        update_data.new_password.encode('utf-8'), 
                        bcrypt.gensalt()
                    ).decode('utf-8')
                    
                    # Usar procedimiento almacenado para restablecer contraseñas
                    cur.execute("SELECT * FROM reset_all_passwords(%s)", 
                               (hashed_password,))
                    
                    result = cur.fetchone()
                    
                    if not result["success"]:
                        conn.rollback()
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=result["message"]
                        )
                    
                    # Si todo salió bien, confirmar la transacción
                    conn.commit()
                    
                    return BulkPasswordUpdateResponse(
                        success=True,
                        count=result["count"],
                        message=result["message"]
                    )
            except Exception as e:
                # Asegurarse de hacer rollback en caso de error
                conn.rollback()
                raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al restablecer contraseñas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contraseñas: {str(e)}"
        )

# Función para cerrar el pool cuando se cierra la aplicación
def close_pool():
    if pool:
        pool.closeall()
