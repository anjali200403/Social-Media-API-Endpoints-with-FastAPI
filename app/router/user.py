from fastapi import APIRouter, FastAPI, HTTPException,status,Depends
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserCreate,UserOut
from ..utils import hash

router=APIRouter( tags=['Users'])


@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate ,db: Session=Depends(get_db)):
    user.password=hash(user.password)
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}",response_model=UserOut)
def get_user(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id ={id} not found")
    return user