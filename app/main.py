from typing import Union,Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.params import Body
import psycopg
from psycopg.rows import dict_row
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .schemas import Post,PostCreate, UserCreated, UserCreatedResponse
from .utils import hash
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


print(settings.db_user)
# try:
#     conn = psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='admin123!')
#     cur = conn.cursor()
#     print("Db conn successfull")
# except Exception as e:
#     print("Connection to db failed error: ",e)


# with psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='admin123!') as conn:
#     with conn.cursor(row_factory=dict_row) as cur:
#         print("db connected successfully")
#         cur.execute('select * from posts')
#         for record in cur:
#             print(record)
    

try:
    conn = psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='admin123!')
    cur = conn.cursor(row_factory=dict_row)
    print("db connected successfully")
except BaseException as e:
    print('issue with the db: ',e)

#     conn.rollback()
# else:
#     conn.commit()
# finally:
#     conn.close()


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [{"title":"Batman","content":"dc superhero","id":1},{"title":"Iron man","content":"marvel superhero","id":2}]
new_post = {}

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# class Post(BaseModel):
#     # id: int
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}






    
