from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from strawberry.asgi import GraphQL
from schema import schema
from controllers.file_controller import router as file_router
from controllers.rest_controller import router as rest_router
from controllers.login_controller import router as login_router

app = FastAPI(title="Campus Virtual API", description="Backend API para Campus Virtual")
prisma = Prisma()

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

# Conectar a la base de datos al iniciar
@app.on_event("startup")
async def startup():
    await prisma.connect()

# Desconectar de la base de datos al cerrar
@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

@app.get("/healthcheck")
async def healthcheck():
    try:
        # Verificar conexión a la base de datos
        await prisma.connect()
        await prisma.role.count()
        await prisma.disconnect()
        return {"status": "ok", "message": "API y base de datos funcionando correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el healthcheck: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)