from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None
    completed: bool | None = False

class TaskEdit(BaseModel):
    id: int
    title: str
    description: str | None

class TaskFromDB(TaskCreate):
    id: int
    created_at: datetime
