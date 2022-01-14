from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
def root():
    return {'message': 'Hello World!'}


@app.get('/posts')
def posts():
    return {'data': 'posts list'}


@app.post('/create-post')
def create_post(data: Post):
    return {'message': f'{data.title} - {data.content} - {data.published} - {data.rating}'}


@app.patch('/update-post')
def update_post():
    return {'message': 'post updated'}


@app.delete('/delete-post')
def delete_post():
    return {'message': 'post deleted'}