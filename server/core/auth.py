from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from models.users import User

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_blacklist = set()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if token in token_blacklist:
            raise JWTError("Token revoked")
        return payload
    except JWTError:
        return None


def revoke_token(token: str):
    token_blacklist.add(token)


def username_exists(username: str, session: Session) -> bool:
    return bool(session.exec(select(User).where(User.username == username)).first())


