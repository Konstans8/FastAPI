# from idlelib.query import Query
# from dataclasses import Field

from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated

from fastapi.params import Depends
# from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse

app = FastAPI()

# @app.get("/")
# async def home() -> str:
#     return 'Hello new page'

# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#
#
# class Post(BaseModel):
#     id: int
#     title: str
#     body: str
#     author: User
#
#
# class PostCreate(BaseModel):
#     title: str
#     body: str
#     author_id: int
#
#
# class UserCreate(BaseModel):
#     name: Annotated[
#         str, Field(..., title='User name', min_length=2, max_length=20)
#     ]
#     age: Annotated[int, Field(..., title='User age', ge=1, le=120)]

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/post/", response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


# users = [
#     {'id': 1, 'name': 'John', 'age': 25},
#     {'id': 2, 'name': 'Mike', 'age': 42},
#     {'id': 3, 'name': 'Luck', 'age': 31}
# ]
#
#
# posts = [
#     {'id': 1, 'title': 'Title 1', 'body': 'News 1', 'author': users[1]},
#     {'id': 2, 'title': 'Title 2', 'body': 'News 2', 'author': users[0]},
#     {'id': 3, 'title': 'Title 3', 'body': 'News 3', 'author': users[2]}
# ]

# @app.get("/items")
# async def items() -> list[Post]:
#     post_objects = []
#     for post in posts:
#         post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
#     return post_objects

# @app.get("/items")
# async def items() -> list[Post]:
#     return [Post(**post) for post in posts]
#
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail='User not found')
#
#     new_post_id = len(posts) + 1
#
#     new_post = posts.append({
#         'id': new_post_id,
#         'title': post.title,
#         'body': post.body,
#         'author': author
#     })
#     posts.append(new_post)
#
#     return Post(**new_post)
#
#
# @app.post("/user/add")
# async def add_user(user: Annotated[
#     UserCreate,
#     Body(..., example={
#         "name": "UserName",
#         "age": 1
#     })
# ]) -> User:
#
#     new_user_id = len(users) + 1
#
#     new_user = {
#         'id': new_user_id,
#         'name': user.name,
#         'age': user.age
#     }
#     users.append(new_user)
#
#     return User(**new_user)
#
#
#
# @app.get("/items/{id}")
# async def items(id: Annotated[int, Path(..., title='for post id', ge=1, lt=100)]) -> Post:
#     for post in posts:
#         if post['id'] == id:
#             return Post(**post)
#     raise HTTPException(status_code=404, detail='Post not found!')
#
#
# @app.get("/search")
# async def search(post_id: Annotated[
#     Optional[int],
#     Query(title='ID of post to search for', ge=1, le=50)
# ]) -> Dict[str, Optional[Post]]:
#     if post_id:
#         for post in posts:
#             if post['id'] == post_id:
#                 return {"data": Post(**post)}
#         raise HTTPException(status_code=404, detail='Post not found')
#     else:
#         return {"data": None}
#
