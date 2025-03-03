import strawberry
from prisma import Prisma
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import uvicorn

prisma = Prisma()

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> list[User]:
        await prisma.connect()
        users = await prisma.user.find_many()
        await prisma.disconnect()
        return [User(id=user.id, name=user.name, email=user.email) for user in users]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User:
        await prisma.connect()
        user = await prisma.user.create(data={"name": name, "email": email})
        await prisma.disconnect()
        return User(id=user.id, name=user.name, email=user.email)
    
    @strawberry.mutation
    async def delete_user(self, id: int) -> bool:
        await prisma.connect()
        await prisma.user.delete(where={"id": id})
        await prisma.disconnect()
        return True
    
    @strawberry.mutation
    async def update_user(self, id: int, name: str, email: str) -> User:
        await prisma.connect()
        user = await prisma.user.update(
            where={"id": id},
            data={"name": name, "email": email}
        )
        await prisma.disconnect()
        return User(id=user.id, name=user.name, email=user.email)

schema = strawberry.Schema(query=Query, mutation=Mutation)


