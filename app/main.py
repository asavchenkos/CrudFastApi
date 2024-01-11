from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.models import Response
from sqlalchemy import text
from sqlalchemy.testing import db
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import News
from starlette.responses import Response

app = FastAPI()
models.Base.metadata.create_all(bind= engine)

@app.post("/posts")
def create(post: News, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts")
def get(db:Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts

@app.delete("/delete/{id}")
def delete(id:int, db:Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    else:
        delete_post.delete(synchronize_session = False)
        db.commit()
    return Response(status_code = status.HTTP_200_OK)

@app.put("/update/{id}")
def update(id:int, post: News, db: Session = Depends(get_db)):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    update_post.first()
    if update_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    else:
        update_post.update(post.dict(), synchronize_session = False)
        db.commit()
    return update_post.first()

@app.get("/get/{id}")
def get(id:int, db:Session = Depends(get_db)):
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
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = {
            "service_status": "up",
            "db_status": "down",
            "db_version": db_version
        })
#TODO : Docker