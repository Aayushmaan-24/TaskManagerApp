from src.user.dtos import UserSchema
from src.user.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_hashed_password(password: str):
    return password_hash.hash(password) 

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