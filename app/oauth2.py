from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

from . import schemas


SECRET_KEY = 'unsecured-secret-key'
ALGORITHM = 'HS256'
TOKEN_VALIDITY = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_VALIDITY)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials', headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token, exception)