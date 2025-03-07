from strawberry.asgi import GraphQL
from schema import schema
from fastapi import FastAPI, HTTPException
import prisma
from models.Roles import RoleBase, RoleResponse
from typing import List
import bcrypt

# print(dir(prisma))

# Encrypt the string "1234" using bcrypt
# password = "1234"
# hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# print(hashed_password)


hashed_password = b'$2b$12$CV9djORsTEcA5/Htw0mWyegU/8y/d6Yn09g4IY9DHHvMDA7xGAYbu'
password = "1234"

if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
    print("La contraseña es correcta.")
else:
    print("La contraseña es incorrecta.")