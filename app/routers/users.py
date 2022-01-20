from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, database


router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash_password(data.password)
    data.password = hashed_password
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/users/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user