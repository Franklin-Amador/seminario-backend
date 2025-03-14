from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from strawberry.asgi import GraphQL
from schema import schema
from controllers.file_controller import router as file_router
from controllers.rest_controller import router as rest_router
from controllers.login_controller import router as login_router
from db import prisma_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    await prisma_client.connect()
    yield  # La aplicación está en ejecución
    # Código que se ejecuta al cerrar la aplicación
    await prisma_client.disconnect()


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

# Añadir la ruta de GraphQL
graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# Incluir los routers
app.include_router(login_router)  # Añadido el router de login
app.include_router(file_router)
app.include_router(rest_router)

@app.get("/")
def read_root():
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
        return {"status": "ok", "message": "API y base de datos funcionando correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el healthcheck: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)