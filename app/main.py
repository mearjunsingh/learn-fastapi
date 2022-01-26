from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .routers import posts, users, vote


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(posts.router)
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(vote.router)


@app.get('/')
def root():
    return {'data': 'Hello World!'}