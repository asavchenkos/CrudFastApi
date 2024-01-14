from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import os
from dotenv import load_dotenv
from . import models
from .database import get_db
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        user = db.query(models.User).get(user_id)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception