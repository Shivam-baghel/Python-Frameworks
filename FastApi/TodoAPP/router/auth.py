from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from model.models import Users
from TodoAPP.helper.database import db_dependency
from passlib.context import CryptContext
from starlette import status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2AuthorizationCodeBearer,
)
import jwt
from jwt import PyJWTError

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "123432123453221eidnfduifsih"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):

    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, userId: int, role: str, expiresDelta: timedelta):

    encode = {"sub": username, "id": userId, "role": role}
    expires = datetime.now(timezone.utc) + expiresDelta
    encode.update({"exp": expires})

    return jwt.encode(payload=encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        userId: int = payload.get("id")
        userRole: str = payload.get("role")

        if username is None or userId is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate user.",
            )

        return {"username": username, "id": userId, "role": userRole}

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user: CreateUserRequest):

    create_user_model = Users(
        email=create_user.email,
        username=create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        role=create_user.role,
        hashed_password=bcrypt_context.hash(create_user.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):

    user = authenticate_user(form_data.username, form_data.password, db)
    
    var: list[int] = [1,2,3]
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user."
        )

    token = create_access_token(
        username=user.username,
        userId=user.id,
        role=user.role,
        expiresDelta=timedelta(minutes=20),
    )

    return {"access_token": token, "token_type": "bearer"}
