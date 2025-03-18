from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# from strawberry.asgi import GraphQL
# from schema import schema

from controllers.high_performance_login_controller import router as login_router

import logging

# Configurar logging para toda la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# class CustomGraphQL(GraphQL):
#     async def process_result(self, request, result):
#         # Log GraphQL errors
#         if result.errors:
#             for error in result.errors:
#                 error_message = str(error)
#                 logger.error(f"GraphQL Error: {error_message}")
        
#         return await super().process_result(request, result)




app = FastAPI(title="Campus Virtual API", description="Backend API para Campus Virtual")


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
# graphql_app = CustomGraphQL(schema)
# app.add_route("/graphql", graphql_app)
# app.add_websocket_route("/graphql", graphql_app)

# Incluir los routers
app.include_router(login_router)

# app.include_router(rest_router)

@app.get("/")
def read_root():
    logger.info("Acceso a la ruta raíz")
    return {
        "message": "Bienvenido a la API del Campus Virtual",
        # "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
