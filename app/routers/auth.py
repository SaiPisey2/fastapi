from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, get_db
from ..schemas import UserLogin,Token
from .. import models,utils,oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login",response_model=Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invlalid Credentials")
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invlalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}
    
    
    
    
