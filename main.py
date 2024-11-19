from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def home() -> str:
    return 'Hello new page'

class Post(BaseModel):
    id: int
    title: str
    body: str

posts = [
    {'id': 1, 'title': 'Title 1', 'body': 'News 1'},
    {'id': 2, 'title': 'Title 2', 'body': 'News 2'},
    {'id': 3, 'title': 'Title 3', 'body': 'News 3'}
]

# @app.get("/items")
# async def items() -> list[Post]:
#     post_objects = []
#     for post in posts:
#         post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
#     return post_objects

@app.get("/items")
async def items() -> list[Post]:
    return [Post(**post) for post in posts]


@app.get("/items/{id}")
async def items(id: int) -> dict:
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=404, detail='Post not found!')


@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return post
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": "No post id provided"}

