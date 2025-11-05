from typing import Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id", check_fields=False)
    def validate_id(cls, id):
        return str(id)



class UpdateTask(BaseModel):
    status: str
    updatedBy: str
    taskTitle: str
    taskDescription: str
    currentOwner: str
class Task(BaseModel):
    taskTitle: str
    taskDescription: str
    payload:str
    currentOwner:str
    createdBy:str
    assignedType: str
    assignedTo: str
    status: str
    updatedBy: str
class TaskIndb(Task,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.now)
    updatedTime: datetime = Field(default_factory=datetime.now)


class TaskHistory(BaseModel):
    taskId: str
    beforeChanges: dict
    afterChanges: dict
    updatedBy: str
    updatedTime: datetime = Field(default_factory=datetime.now)
    comment: str

