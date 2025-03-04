import strawberry
from prisma import Prisma
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import uvicorn

from typing import List, Optional

prisma = Prisma()

@strawberry.type
class Role:
    id: int
    name: str
    shortname: str
    description: Optional[str]
    sortorder: int
    archetype: Optional[str]

@strawberry.type
class Query:
    @strawberry.field
    async def roles(self) -> List[Role]:
        await prisma.connect()
        roles = await prisma.role.find_many()
        await prisma.disconnect()
        return [Role(
            id=role.id,
            name=role.name,
            shortname=role.shortname,
            description=role.description,
            sortorder=role.sortorder,
            archetype=role.archetype
        ) for role in roles]

    @strawberry.field
    async def role(self, role_id: int) -> Role:
        await prisma.connect()
        role = await prisma.role.find_unique(where={"id": role_id})
        await prisma.disconnect()
        if not role:
            raise Exception("Role not found")
        return Role(
            id=role.id,
            name=role.name,
            shortname=role.shortname,
            description=role.description,
            sortorder=role.sortorder,
            archetype=role.archetype
        )

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_role(
        self,
        name: str,
        shortname: str,
        sortorder: int,
        description: Optional[str] = None,
        archetype: Optional[str] = None
    ) -> Role:
        await prisma.connect()
        new_role = await prisma.role.create(data={
            "name": name,
            "shortname": shortname,
            "description": description,
            "sortorder": sortorder,
            "archetype": archetype
        })
        await prisma.disconnect()
        return Role(
            id=new_role.id,
            name=new_role.name,
            shortname=new_role.shortname,
            description=new_role.description,
            sortorder=new_role.sortorder,
            archetype=new_role.archetype
        )

    @strawberry.mutation
    async def update_role(
        self,
        role_id: int,
        name: Optional[str] = None,
        shortname: Optional[str] = None,
        description: Optional[str] = None,
        sortorder: Optional[int] = None,
        archetype: Optional[str] = None
    ) -> Role:
        await prisma.connect()
        updated_role = await prisma.role.update(
            where={"id": role_id},
            data={
                "name": name,
                "shortname": shortname,
                "description": description,
                "sortorder": sortorder,
                "archetype": archetype
            }
        )
        await prisma.disconnect()
        if not updated_role:
            raise Exception("Role not found")
        return Role(
            id=updated_role.id,
            name=updated_role.name,
            shortname=updated_role.shortname,
            description=updated_role.description,
            sortorder=updated_role.sortorder,
            archetype=updated_role.archetype
        )

    @strawberry.mutation
    async def delete_role(self, role_id: int) -> Role:
        await prisma.connect()
        deleted_role = await prisma.role.delete(where={"id": role_id})
        await prisma.disconnect()
        if not deleted_role:
            raise Exception("Role not found")
        return Role(
            id=deleted_role.id,
            name=deleted_role.name,
            shortname=deleted_role.shortname,
            description=deleted_role.description,
            sortorder=deleted_role.sortorder,
            archetype=deleted_role.archetype
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)


