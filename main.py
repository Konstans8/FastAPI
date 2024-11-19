from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def home() -> str:
    return 'Hello new page'

class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


users = [
    {'id': 1, 'name': 'John', 'age': 25},
    {'id': 2, 'name': 'Mike', 'age': 42},
    {'id': 3, 'name': 'Luck', 'age': 31}
]


posts = [
    {'id': 1, 'title': 'Title 1', 'body': 'News 1', 'author': users[1]},
    {'id': 2, 'title': 'Title 2', 'body': 'News 2', 'author': users[0]},
    {'id': 3, 'title': 'Title 3', 'body': 'News 3', 'author': users[2]}
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
async def items(id: int) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found!')


@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": None}

