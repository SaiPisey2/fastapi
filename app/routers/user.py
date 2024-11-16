from .. import models
from ..utils import hash
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..schemas import Post,PostCreate, UserCreated, UserCreatedResponse
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserCreatedResponse)
def create_user(user: UserCreated ,db: Session = Depends(get_db)):

    hashed_pass = hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=UserCreatedResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} doesnt exists")

    return user