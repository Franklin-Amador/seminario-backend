from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from strawberry.asgi import GraphQL
from schema import schema
from controllers.file_controller import router as file_router
# from controllers.rest_controller import router as rest_router
from controllers.login_controller import router as login_router
from controllers.assignaments_controllers import router as assignaments_router
from controllers.courses_controller import router as courses_router
from controllers.claifications_controller import router as califications_router
from controllers.sections_controller import router as sections_router
from controllers.user_controller import router as user_router
from controllers.role_controller import router as role_router
from controllers.forum_controller import router as forum_controller 
from controllers.enrrollments_controller import router as enrollments_router
from controllers.summision_controller import router as summision_router
from controllers.category_controller import router as category_router


from db import prisma_client
import logging

# Configurar logging para toda la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

class CustomGraphQL(GraphQL):
    async def process_result(self, request, result):
        # Log GraphQL errors
        if result.errors:
            for error in result.errors:
                error_message = str(error)
                logger.error(f"GraphQL Error: {error_message}")
        
        return await super().process_result(request, result)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    logger.info("Conectando a la base de datos...")
    await prisma_client.connect()
    logger.info("Conexión a la base de datos establecida")
    yield  # La aplicación está en ejecución
    # Código que se ejecuta al cerrar la aplicación
    logger.info("Cerrando conexión a la base de datos...")
    await prisma_client.disconnect()
    logger.info("Conexión a la base de datos cerrada")


app = FastAPI(title="Campus Virtual API", description="Backend API para Campus Virtual", lifespan=lifespan)


# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    # Añadir aquí los dominios de producción cuando corresponda
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware para registrar todas las solicitudes
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Añadir la ruta de GraphQL con la versión personalizada que hace logging de errores
graphql_app = CustomGraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# Incluir los routers
app.include_router(login_router)  # Añadido el router de login
app.include_router(file_router)
app.include_router(courses_router)
app.include_router(forum_controller)
app.include_router(assignaments_router)
app.include_router(sections_router)
app.include_router(califications_router)
app.include_router(user_router)
app.include_router(enrollments_router)
app.include_router(role_router)
app.include_router(summision_router)
app.include_router(category_router)

# app.include_router(rest_router)

@app.get("/")
def read_root():
    logger.info("Acceso a la ruta raíz")
    return {
        "message": "Bienvenido a la API del Campus Virtual",
        "docs": "/docs",
        "graphql": "/graphql"
    }

@app.get("/healthcheck")
async def healthcheck():
    try:
        # Verificar conexión a la base de datos     
        await prisma_client.role.count()
        logger.info("Healthcheck ejecutado correctamente")
        return {"status": "ok", "message": "API y base de datos funcionando correctamente"}
    except Exception as e:
        error_msg = f"Error en el healthcheck: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
