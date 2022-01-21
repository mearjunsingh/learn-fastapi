from fastapi import FastAPI

from . import models, database
from .routers import posts, users, vote


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(posts.router)
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(vote.router)


@app.get('/')
def root():
    return {'data': 'Hello World!'}