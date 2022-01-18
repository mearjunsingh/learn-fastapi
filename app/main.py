from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


@app.get('/')
def root():
    return {'data': 'Hello World!'}


@app.get('/posts')
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(data: Post, db: Session = Depends(get_db)):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {'data': post}


@app.get('/posts/{id}')
def read_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return {'data': post}


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, data: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return {'data': post.first()}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    post.delete(synchronize_session=False)
    db.commit()
    return {'data': f'Post with id {id} deleted'}