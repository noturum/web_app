from typing import List, Union

from fastapi import (APIRouter,
                     HTTPException,
                     Depends)
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from models.user import TUser, UserModel
from main.middlewares.jwt import create_access_token, validate_token
from pydantic import BaseModel

api = APIRouter()


class TokenModel(BaseModel):
    access_token: str
    token_type: str


@api.post("/oauth/token", response_model=TokenModel)
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends()):
    user: TUser = await TUser.get_by_username(form.username)
    if user and user[0].verify_password(form.password):
        access_token = create_access_token(data={"sub": user[0].username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid pass or usrname",
        )


@api.post("/users/", response_model=UserModel)
async def create_user(form: UserModel):
    user = TUser()
    user.username = form.username
    user.hash_password(form.password)
    await user.save()
    return user


@api.get("/users/", response_model=List[UserModel])
async def get_users(ouath: bool = Depends(validate_token)):
    users = await TUser.all()
    return users


@api.put("/users/{user_id}", response_model=UserModel)
async def update_user(user_id: int, form: UserModel, ouath: bool = Depends(validate_token)):
    user: TUser = await TUser.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = form.username
    user.hash_password(form.password)
    await user.save()
    return user


@api.delete("/users/{user_id}")
async def delete_user(user_id: int, ouath: bool = Depends(validate_token)):
    user: TUser = await TUser.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user.remove()
    return {"message": "User deleted successfully"}
