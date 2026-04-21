from typing import Annotated, Generator
from app.core import security
import jwt
from app.core.db import engine
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.utils.config import settings
from app.models.users import Usuario
from app.models.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token"
)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> Usuario:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pudo validar las credenciales",
        )
    
    user = session.get(Usuario, token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user


CurrentUser = Annotated[Usuario, Depends(get_current_user)]

