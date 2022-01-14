from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def root():
    return {'message' : 'Hello World!'}


@app.get('/posts')
def posts():
    return {'data' : 'posts list'}


@app.post('/create-post')
def create_post():
    return {'message' : 'post created'}


@app.patch('/update-post')
def update_post():
    return {'message' : 'post updated'}


@app.delete('/delete-post')
def delete_post():
    return {'message' : 'post deleted'}