from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str
    
class UserReg(UserLogin):
    email: EmailStr | None
