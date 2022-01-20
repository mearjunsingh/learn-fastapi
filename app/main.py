from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, utils
from .database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return {'data': 'Hello World!'}


@app.get('/posts', response_model=List[schemas.Post])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get('/posts/{id}', response_model=schemas.Post)
def read_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return post


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, data: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    post.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Post with id {id} deleted'}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(data.password)
    data.password = hashed_password
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/users/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user