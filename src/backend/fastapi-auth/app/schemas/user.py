from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password:str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id:id
    name:str
    email:EmailStr
    model_config = ConfigDict(from_attributes=True)


