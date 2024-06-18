from pydantic import BaseModel

class CreateTokenSchema(BaseModel):
    email: str
    password: str

class TokenSchema(BaseModel):
    token: str

class TokenValidateResponseSchema(BaseModel):
    user_id: int
