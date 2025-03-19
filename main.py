from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter
import uvicorn
import logging

# Importar los controladores existentes
from controllers.high_performance_login_controller import login, update_password, reset_all_passwords
from controllers.high_performance_login_controller import LoginRequest, LoginResponse, BulkPasswordUpdateRequest, BulkPasswordUpdateResponse, UpdatePasswordRequest

# Importar nuestro esquema GraphQL y la conexión a BD
from schema import schema
from db import close_pool, Database

# Configurar logging para toda la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Función de lifespan para gestionar la inicialización y cierre de recursos
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta antes de iniciar la aplicación
    logger.info("Iniciando aplicación...")
    try:
        # Verificar la conexión a la base de datos
        pool = Database.get_pool()
        if pool:
            logger.info("Pool de conexiones verificado")
        else:
            logger.warning("El pool de conexiones no está disponible")
    except Exception as e:
        logger.error(f"Error al verificar el pool de conexiones: {str(e)}")
    
    yield  # Aquí se ejecuta la aplicación
    
    # Código que se ejecuta al cerrar la aplicación
    logger.info("Cerrando aplicación...")
    try:
        close_pool()
        logger.info("Recursos liberados correctamente")
    except Exception as e:
        logger.error(f"Error al liberar recursos: {str(e)}")

# Crear la aplicación FastAPI con el lifespan
app = FastAPI(
    title="Campus Virtual API", 
    description="Backend API para Campus Virtual",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de solicitudes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

# Añadir la ruta GraphQL
graphql_router = GraphQLRouter(schema)
app.include_router(graphql_router, prefix="/graphql")

# Rutas existentes para login
@app.post("/api/login", response_model=LoginResponse)
async def login_endpoint(request: Request, login_data: LoginRequest):
    return await login(login_data, request)

@app.put("/api/update_password", response_model=LoginResponse)
async def update_password_endpoint(update_data: UpdatePasswordRequest):
    return await update_password(update_data)

@app.put("/api/reset_all_passwords", response_model=BulkPasswordUpdateResponse)
async def reset_all_passwords_endpoint(update_data: BulkPasswordUpdateRequest):
    return await reset_all_passwords(update_data)

# Ruta de verificación de estado
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

# Ruta raíz
@app.get("/")
def read_root():
    logger.info("Acceso a la ruta raíz")
    return {
        "message": "Bienvenido a la API del Campus Virtual",
        "docs": "/docs",
        "graphql": "/graphql"
    }

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    logger.info("Iniciando servidor...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
