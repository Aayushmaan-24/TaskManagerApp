from src.user.dtos import UserSchema
from src.user.models import UserModel
from sqlalchemy.orm import Session


def register_user(body: UserSchema, db:Session):
    print(body)
    return "User registered successfully"