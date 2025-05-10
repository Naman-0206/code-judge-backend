from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from uuid import uuid4
from datetime import datetime, timedelta
from core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, verify_password,
    create_access_token, decode_token, revoke_token, username_exists
)
from models.users import User
from core.db import get_session
from schemas.users import UserCreate, UserLogin, Token


router = APIRouter(
    prefix="",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if username_exists(user.username, session):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        password=hashed_pw
    )
    session.add(new_user)
    session.commit()
    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(
        User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token}


@router.post("/logout")
def logout(request: Request, token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"message": "Logged out successfully"}
