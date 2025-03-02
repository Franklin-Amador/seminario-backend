import strawberry
from prisma import Prisma

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

schema = strawberry.Schema(query=Query, mutation=Mutation)