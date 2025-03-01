from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

from model.models import Users
from sqlalchemy.orm import Session
from database import  db_dependency
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/users',
    tags=['user']
)


user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    newPassword: str = Field(min_length=6)
    reEnterNewPassword: str = Field(min_length=6)



@router.get("/", status_code= status.HTTP_200_OK)
async def get_user(user: user_dependency, db : db_dependency):
    
    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    
    return db.query(Users).filter(Users.owner_id == user.get('id')).first()




@router.put("/change_password", status_code= status.HTTP_204_NO_CONTENT)
async def get_user(user: user_dependency, db : db_dependency,
                   user_verification: UserVerification):
    
    if not user_verification.newPassword == user_verification.reEnterNewPassword:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= 'Error on password')
    
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Authorization failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail='Password does not match')
    
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.newPassword)
    db.add(user_model)
    
    db.commit()
