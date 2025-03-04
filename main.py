
from strawberry.asgi import GraphQL
from schema import schema
from fastapi import FastAPI, HTTPException
from prisma import Prisma
from models.Roles import RoleBase, RoleResponse
from typing import List



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

# * Endpoint para crear un nuevo usuario
# @app.post("/users", response_model=UserResponse)
# async def create_user(user: UserBase):
#     new_user = await prisma.user.create(data={"name": user.name, "email": user.email})
#     return new_user


# Crear un nuevo rol
@app.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleBase):
    new_role = await prisma.role.create(data=role.dict())
    return new_role

# Obtener todos los roles
@app.get("/roles", response_model=List[RoleResponse])
async def get_roles():
    roles = await prisma.role.find_many()
    return roles

@app.get("/debug")
async def debug():
    return {"models": dir(prisma)}


# Obtener un rol por ID
@app.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int):
    role = await prisma.role.find_unique(where={"id": role_id})
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Actualizar un rol
@app.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleBase):
    updated_role = await prisma.role.update(
        where={"id": role_id},
        data=role.dict()
    )
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

# Eliminar un rol
@app.delete("/roles/{role_id}", response_model=RoleResponse)
async def delete_role(role_id: int):
    deleted_role = await prisma.role.delete(where={"id": role_id})
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role