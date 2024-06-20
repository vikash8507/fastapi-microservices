from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserDetail(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    token: str

    class Config:
        orm_mode = True

class CreateTokenSchema(BaseModel):
    email: str
    password: str
