from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter
import uvicorn
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Importar los controladores
import controllers.user_controller as user_controller
import controllers.courses_controller as courses_controller
import controllers.category_controller as category_controller
import controllers.assignments_controller as assignments_controller
import controllers.submission_controller as submission_controller
import controllers.grades_controller as grades_controller
import controllers.enrollments_controller as enrollments_controller
import controllers.forum_controller as forum_controller
import controllers.resources_controller as resources_controller
import controllers.role_controller as role_controller
import controllers.sections_controller as sections_controller
import controllers.file_controller as file_controller
import controllers.login_controller as login_controller

# Importar para GraphQL
try:
    from schema import schema
    from db import close_pool, Database
    has_graphql = True
except ImportError:
    has_graphql = False
    logging.warning("GraphQL schema not found. GraphQL functionality will be disabled.")

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
    if has_graphql:
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
    if has_graphql:
        try:
            close_pool()
            logger.info("Recursos liberados correctamente")
        except Exception as e:
            logger.error(f"Error al liberar recursos: {str(e)}")

# Crear la aplicación FastAPI con el lifespan
app = FastAPI(
    title="Campus Virtual API",
    description="API para gestionar un campus virtual educativo",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los dominios permitidos
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

# Manejador de errores personalizado
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error interno: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Error interno del servidor: {str(exc)}"}
    )

# Añadir GraphQL router si está disponible
if has_graphql:
    graphql_router = GraphQLRouter(schema)
    app.include_router(graphql_router, prefix="/graphql")
    logger.info("GraphQL router configurado y disponible en /graphql")

# Incluir los routers de los controladores REST
app.include_router(user_controller.router)
app.include_router(courses_controller.router)
app.include_router(category_controller.router)
app.include_router(assignments_controller.router)
app.include_router(submission_controller.router)
app.include_router(grades_controller.router)
app.include_router(enrollments_controller.router)
app.include_router(forum_controller.router)
app.include_router(resources_controller.router)
app.include_router(role_controller.router)
app.include_router(sections_controller.router)
app.include_router(file_controller.router, tags=["files"])
app.include_router(login_controller.router, tags=["login"])

# Rutas existentes para login desde high_performance_login_controller 
# (solo se utilizan si se detecta el módulo)
try:
    from controllers.high_performance_login_controller import login, update_password, reset_all_passwords
    from controllers.high_performance_login_controller import LoginRequest, LoginResponse, BulkPasswordUpdateRequest, BulkPasswordUpdateResponse, UpdatePasswordRequest
    
    @app.post("/api/login", response_model=LoginResponse)
    async def login_endpoint(request: Request, login_data: LoginRequest):
        return await login(login_data, request)

    @app.put("/api/update_password", response_model=LoginResponse)
    async def update_password_endpoint(update_data: UpdatePasswordRequest):
        return await update_password(update_data)

    @app.put("/api/reset_all_passwords", response_model=BulkPasswordUpdateResponse)
    async def reset_all_passwords_endpoint(update_data: BulkPasswordUpdateRequest):
        return await reset_all_passwords(update_data)
        
    logger.info("High performance login endpoints configurados")
except ImportError:
    logger.info("High performance login controller no encontrado, usando controlador estándar")

# Ruta raíz
@app.get("/")
async def root():
    logger.info("Acceso a la ruta raíz")
    if has_graphql:
        return {
            "message": "Campus Virtual API está en funcionamiento",
            "docs": "/docs",
            "graphql": "/graphql"
        }
    else:
        return {
            "message": "Campus Virtual API está en funcionamiento",
            "docs": "/docs"
        }

# Ruta de verificación de estado
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Ejecutar el servidor (si se ejecuta directamente)
if __name__ == "__main__":
    logger.info("Iniciando servidor...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)