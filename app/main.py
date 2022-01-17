from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from . import models
from .database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


posts_list = [
    {
        'title': 'post 1',
        'content': 'content 1',
        'published': True,
        'rating': 5,
        'id': 1
    },
    {
        'title': 'post 2',
        'content': 'content 2',
        'published': False,
        'rating': None,
        'id': 2
    }
]


def validate_id(id):
    if id <= 0: # because array index starts with 0
        return None
    else:
        return id - 1


@app.get('/')
def root():
    return {'data': 'Hello World!'}


@app.get('/posts')
def list_posts():
    return {'data': posts_list}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    data_dict = data.dict()
    data_dict['id'] = len(posts_list) + 1
    posts_list.append(data_dict)
    return {'data': data_dict}


@app.get('/posts/{id}')
def read_post(id: int, response: Response):
    try:
        post = posts_list[validate_id(id)]
        return {'data': post}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'post with id {id} not found'}


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, data: Post):
    try:
        data_dict = data.dict()
        posts_list[validate_id(id)] = data_dict
        data_dict['id'] = id
        return {'data': data_dict}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        posts_list[(validate_id(id))] = None
        return {'data': f'post with id {id} deleted'}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')


@app.get('/sql')
def sql(db: Session = Depends(get_db)):
    return {'status': 'success'}