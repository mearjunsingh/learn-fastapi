from fastapi import FastAPI, Body


app = FastAPI()


@app.get('/')
def root():
    return {'message' : 'Hello World!'}


@app.get('/posts')
def posts():
    return {'data' : 'posts list'}


@app.post('/create-post')
def create_post(data: dict = Body(...)):
    data['message'] = 'post created'
    return data


@app.patch('/update-post')
def update_post():
    return {'message' : 'post updated'}


@app.delete('/delete-post')
def delete_post():
    return {'message' : 'post deleted'}