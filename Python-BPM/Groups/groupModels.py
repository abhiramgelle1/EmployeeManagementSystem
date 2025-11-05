from typing import Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id", check_fields=False)
    def validate_id(cls, id):
        return str(id)

class Group(BaseModel):
    groupName:str
    description:str
class GroupIndb(Group,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.now)
    updatedTime: datetime = Field(default_factory=datetime.now)





