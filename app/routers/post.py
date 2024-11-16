from .. import models
from ..utils import hash
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..schemas import Post,PostCreate, UserCreated, UserCreatedResponse
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Union,Optional, List
from .. import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = "" ):
    # cur.execute('select * from posts')
    # posts = cur.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() ## to get all post from specific user
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id)
    return posts

@router.get("/{id}", response_model=Post)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute("select * from posts where id = %s",(id,))
    # returned_post = cur.fetchone()

    returned_post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not returned_post:
        raise HTTPException(status_code=404,detail=f"post with id:{id} doesnt exists")
    
    if returned_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the action")
    
    return returned_post

    

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@router.post("/{id}",status_code=status.HTTP_201_CREATED,response_model=Post)
def create_posts(post: PostCreate,id=id,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):


    # cur.execute("insert into posts (title,content,published) values (%s,%s,%s) returning *",(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # ---> ** unpacking operator, unpacks the values in the dict, each key value pair is passed as keyword arguement
    '''
    for eg post.model_dump() gives {'title':'1','content':'1 content'}
    models.Post(title =1, content = '1 content')
    '''
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute("delete from posts where id = %s returning *",(id,))
    # deleted_post = cur.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id==id)
    post = deleted_post.first()

    if post == None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} not found")  
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"result": "post deleted"}


    

@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute("update posts set title = %s,content = %s, published=%s where id = %s returning *",(post.title,post.content,post.published,id))
    # updated_post = cur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_updated = post_query.first()
    if not post_updated:
        raise HTTPException(status_code=404,detail=f"post with id:{id} doesnt exists")
    
    if post_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the action")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()