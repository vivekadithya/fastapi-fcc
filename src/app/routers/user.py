from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, utils
from ..schemas import UserCreate, UserOut
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session=Depends(get_db)):

    new_user = db.query(models.User).filter(models.User.email==user.email)

    if new_user.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"{user.email} in system.")

    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump()) # The ** takes care of extracting the properties and assigning them to the Columns

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[UserOut])
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)

    if not user.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User: {id} not found.")
    return user.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User: {id} not found.")
    
    user.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)