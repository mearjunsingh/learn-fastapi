from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = 'unsecured-secret-key'
ALGORITHM = 'HS256'
TOKEN_VALIDITY = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_VALIDITY)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt