from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, database, oauth2


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=List[schemas.PostOut])
def list_posts(limit: int = 10, skip: int = 0, search: Optional[str] = '', db: Session = Depends(database.get_db)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(data: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(user_id = current_user.id, **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/{id}', response_model=schemas.PostOut)
def read_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, data: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission Denied')
    post.update(data.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission Denied')
    post.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Post with id {id} deleted'}