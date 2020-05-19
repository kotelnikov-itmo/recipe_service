from jwt import PyJWTError

from fastapi import exceptions, status, Depends
from fastapi.security import OAuth2PasswordBearer

from db import get_db
from auth.backend import get_payload
from auth.services import UserService
from auth.models import User
from .schemas import UserTokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/--swagger-auth",
                                     auto_error=False)

_exception = exceptions.HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(db=Depends(get_db),
                           token: str = Depends(oauth2_scheme)
                           ) -> User:
    try:
        token_data = UserTokenData(**get_payload(token))
        username: str = token_data.sub
        if username is None:
            raise _exception
    except (PyJWTError, ValueError):
        raise _exception
    user = UserService(db).get_user(username=username)
    if user is None:
        raise _exception
    else:
        return user
