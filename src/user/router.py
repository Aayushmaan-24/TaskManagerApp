from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller


user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model=[UserResponseSchema], status_code=status.HTTP_201_CREATED)
def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register_user(body, db)

@user_routes.post("/login", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)