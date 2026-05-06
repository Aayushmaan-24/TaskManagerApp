from math import exp
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from src.user.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()

def get_hashed_password(password: str):
    return password_hash.hash(password) 

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def register_user(body: UserSchema, db:Session):
    
    # email validation
    is_user_exist = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    # user name validation
    is_user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    
    hashed_password = get_hashed_password(body.password)
    new_user = UserModel(
        name = body.name,
        username = body.username,
        email = body.email,
        hashed_password = hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def login_user(body: UserLoginSchema, db: Session):
        is_user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()
        
        if not is_user_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
        
        if not verify_password(body.password, is_user_exist.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
        
        expire_time = datetime.now() + timedelta(seconds=settings.EXP_TIME)
        
        token = jwt.encode({"_id":is_user_exist.id, "username":is_user_exist.username, "exp":expire_time}, settings.SECRET_KEY , settings.ALGORITHM)
        
        return {
            "token":token
            }
        
        