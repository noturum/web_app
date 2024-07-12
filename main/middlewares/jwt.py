from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from starlette import status

from main.middlewares.secrets import EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models.user import TUser

oauth_param = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    encode_data = data.copy()
    encode_data.update({"exp": datetime.now() + timedelta(minutes=EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(token: str = Depends(oauth_param)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await TUser.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
