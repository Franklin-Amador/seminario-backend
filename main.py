
from strawberry.asgi import GraphQL
from schema import schema
from fastapi import FastAPI, HTTPException
from prisma import Prisma
from models.User import UserBase, UserResponse

app = FastAPI()
prisma = Prisma()

# # Ruta para GraphQL
app.add_route("/graphql", GraphQL(schema))

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with GraphQL and Prisma!"}

# Conectar y desconectar Prisma automáticamente
@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

# * Endpoint para obtener todos los usuarios
@app.get("/users", response_model=list[UserResponse])
async def get_users():
    users = await prisma.user.find_many()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# * Endpoint para obtener un usuario por ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# * Endpoint para crear un nuevo usuario
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserBase):
    new_user = await prisma.user.create(data={"name": user.name, "email": user.email})
    return new_user

# * Endpoint para actualizar un usuario
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserBase):
    updated_user = await prisma.user.update(where={"id": user_id}, data={"name": user.name, "email": user.email})
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# * Endpoint para eliminar un usuario
@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    deleted_user = await prisma.user.delete(where={"id": user_id})
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user