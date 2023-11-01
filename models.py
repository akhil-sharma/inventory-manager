from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    user_id: str

class UserInDB(UserBase):
    user_id: str
    password_hash: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_Id: str | None = None
