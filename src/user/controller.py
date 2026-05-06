from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from src.user.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, status
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
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
    
    hashed_password = get_hashed_password(body.hashed_password)
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
        
        exp_time = datetime.now() + timedelta(seconds=settings.EXP_TIME)
        
        token = jwt.encode({"_id":is_user_exist.id, "username":is_user_exist.username, "exp":exp_time.timestamp()}, settings.SECRET_KEY , settings.ALGORITHM)
        
        return UserResponseSchema(
            id=is_user_exist.id,
            name=is_user_exist.name,
            username=is_user_exist.username,
            email=is_user_exist.email,
        )
        

def is_authenticated(request: Request, db: Session):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        
        user_id = data.get("_id")
        exp_time = data.get("exp")
        
        current_time = datetime.now().timestamp()
        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")