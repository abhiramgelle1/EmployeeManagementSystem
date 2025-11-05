from typing import Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id", check_fields=False)
    def validate_id(cls, id):
        return str(id)



class UserLogin(BaseModel):
    username: str
    password: str
class User(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    dateOfBirth: str
    status:str
    manager: str = None
    role: str
    pan:str
    aadhar: str
    passport:str
    displayPicture: str
class UserIndb(User,DBModelMixin):
    joiningDate: datetime = Field(default_factory=datetime.now)
    releasingDate: datetime = None
class UpdateUser(UserLogin):
    newPassword: str