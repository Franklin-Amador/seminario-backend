from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str
    shortname: str
    description: Optional[str] = None
    sortorder: int
    archetype: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True