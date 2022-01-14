from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


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


@app.post('/posts')
def create_post(data: Post):
    data_dict = data.dict()
    data_dict['id'] = len(posts_list) + 1
    posts_list.append(data_dict)
    return {'data': data_dict}


@app.get('/posts/{id}')
def read_post(id: int):
    try:
        post = posts_list[validate_id(id)]
        return {'data': post}
    except:
        return {'data': None}


@app.put('/posts/{id}')
def update_post(id: int, data: Post):
    try:
        data_dict = data.dict()
        posts_list[validate_id(id)] = data_dict
        data_dict['id'] = id
        return {'data': data_dict}
    except:
        return {'data': None}


@app.delete('/posts/{id}')
def delete_post(id: int):
    try:
        posts_list[(validate_id(id))] = None
        return {'data': f'post with id {id} deleted'}
    except:
        return {'data': None}