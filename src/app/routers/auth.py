from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, schemas, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
                            f"Invalid Credentials")
    verified = utils.verify(user_credentials.password, user.password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
                            f"Invalid Credentials")
    # create & return token
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
     