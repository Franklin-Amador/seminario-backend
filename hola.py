from strawberry.asgi import GraphQL
from schema import schema
from fastapi import FastAPI, HTTPException
import prisma
from models.Roles import RoleBase, RoleResponse
from typing import List

print(dir(prisma))
