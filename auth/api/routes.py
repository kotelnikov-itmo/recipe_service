from fastapi import Depends, status, exceptions, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from db import get_db
from auth.services import UserService
from auth.backend import ACCESS_TOKEN_EXPIRE, authenticate_user, create_access_token
from auth.api.schemas import (
    UserProfileSchema, UserCreateSchema, UserAuthCredentialsSchema,
    ResponseWithToken, UserTokenData
)


router = APIRouter()


@router.post("/users", response_model=UserProfileSchema)
async def create_user(user_data: UserCreateSchema,
                      db=Depends(get_db)):
    """Регистрация нового пользователя;
    """
    user = UserService(db).create_user(**user_data.dict())
    return user


@router.post('/token', response_model=ResponseWithToken,
             response_description=f"Return JWT token with user data; lifetime {ACCESS_TOKEN_EXPIRE}s")
async def obtain_token(credentials: UserAuthCredentialsSchema, db=Depends(get_db)) -> ResponseWithToken:
    """
    Get access token by credentials
    """
    user = authenticate_user(db, **credentials.dict())
    if not user:
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    token = create_access_token(UserTokenData(sub=user.username).dict())
    return ResponseWithToken(token=token)


@router.post('/--swagger-auth')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """For support doc-view authorization"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(UserTokenData(sub=user.username).dict())
    return {"access_token": access_token, "token_type": "bearer"}