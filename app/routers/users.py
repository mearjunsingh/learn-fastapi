from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, database, oauth2


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash_password(data.password)
    data.password = hashed_password
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user


@router.post('/login', response_model=schemas.Token)
def login_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    if utils.verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Mistake")
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}