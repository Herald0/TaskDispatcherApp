from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    
class UserFromDB(UserCreate):
    id: int
