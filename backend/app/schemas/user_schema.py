from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    is_approved: bool
    role: str
    
class UserRegister(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

class UserLogIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenRequest(BaseModel):
    token: str

class UserDisplay(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr

class UserTeamAdd(BaseModel):
    user_id: int
    team_id: int