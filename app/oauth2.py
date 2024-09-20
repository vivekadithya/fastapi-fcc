from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id: int = payload.get("user_id")

        if not id:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token=token, credential_exception=credential_exception)

    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    return current_user