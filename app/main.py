from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.models import Response
from sqlalchemy import text
import uvicorn

from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import News, UserBase
from starlette.responses import Response
from app.oauth2 import get_current_user, oauth2_scheme
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app.logger_config import logger, LoggingMiddleware


load_dotenv()


app = FastAPI()
models.Base.metadata.create_all(bind= engine)

# Add the middleware to the FastAPI application
app.add_middleware(LoggingMiddleware)

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define your SECRET_KEY and ALGORITHM
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

@app.post("/register")
def register(user: UserBase, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        logger.info(f"Attempt to register an existing user: {user.username}")
        return {"message": "User already exists."}
    hashed_password = user.password  #pwd_context.hash(user.password) - to hash a password
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New user registered: {user.username}")
    return {"message": "User created successfully."}

@app.post("/login")
def login(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user : #or not pwd_context.verify(user.password, db_user.hashed_password) - to verify hashed password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a payload dictionary
    payload = {
        "sub": str(db_user.id),  # subject
        "iat": datetime.utcnow(),  # issued at
        "exp": datetime.utcnow() + timedelta(minutes=15)  # expires at
    }

    # Generate a JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "?"}

@app.post("/posts")
def create(post: News, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts")
def get(db:Session = Depends(get_db), user: str = Depends(get_current_user)):
    all_posts = db.query(models.Post).all()
    return all_posts

@app.delete("/delete/{id}")
def delete(id:int, db:Session = Depends(get_db), user: str = Depends(get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    else:
        delete_post.delete(synchronize_session = False)
        db.commit()
    return Response(status_code = status.HTTP_200_OK)

@app.put("/update/{id}")
def update(id:int, post: News, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    update_post.first()
    if update_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    else:
        update_post.update(post.dict(), synchronize_session = False)
        db.commit()
    return update_post.first()

@app.get("/get/{id}")
def get(id:int, db:Session = Depends(get_db), user: str = Depends(get_current_user)):
    solo_post = db.query(models.Post).filter(models.Post.id == id)
    if solo_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    else:
        return solo_post.first()

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    db_status = "down"
    service_status = "down"
    db_version = "Unknown"
    try:
        # Check DB connection
        db.execute(text('SELECT 1'))
        db_status = "up"

        # Get DB version
        result = db.execute(text('SELECT version()'))
        db_version = result.first()[0] if result else "Unknown"

        # If the above operations are successful, it means the service is up
        service_status = "up"
    except Exception as e:
        pass

    if service_status == "up" and db_status == "up":
        return {
            "service_status": "up",
            "db_status": "up",
            "db_version": db_version
        }
    else:
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = {
            "service_status": "up",
            "db_status": "down",
            "db_version": db_version
        })


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

#TODO : Docker
