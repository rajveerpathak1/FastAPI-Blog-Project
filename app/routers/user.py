from passlib.context import CryptContext

from .. import models,schemas
from fastapi import FastAPI, Depends, HTTPException, Response, status , Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from ..database import get_db
from .. import utils





router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", response_model=schemas.ResponseUser)
def create_user(data: schemas.User, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    h_pass = utils.HashPass(data.password)
    data.password = h_pass
    user_data = models.User(**data.dict())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@router.get("/{id}" ,response_model=schemas.ResponseUser)
def get_user(id : int , db:Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=404,detail=f"Details of user with id = {id} not found")
    return user_data
