from pydantic import BaseModel

class UserSchema(BaseModel):

    name: str
    user: str
    password: str
    email: str

class Config:
    orm_mode = True