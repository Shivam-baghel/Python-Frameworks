from fastapi import APIRouter
from pydantic import BaseModel
from model.models import Users
from database import db_dependency

router = APIRouter()


class CreateUserRequest(BaseModel):
    
    username: str 
    email: str 
    first_name : str 
    last_name: str
    password: str
    role: str
    
    
    

@router.post("/auth")
async def create_user(create_user: CreateUserRequest):
    
    create_user_model = Users(
        email=create_user.email,
        username=create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        role=create_user.role,
        hashed_password = create_user.password,
        is_active=True
    )
    
    return create_user_model