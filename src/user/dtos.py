from pydantic import BaseModel

class UserSchema(BaseModel):

    name: str
    username: str
    hashed_password: str
    email: str

class UserResponseSchema(BaseModel):
    name: str
    username: str
    email: str
    id: int