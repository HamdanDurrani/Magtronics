from fastapi import APIRouter, Depends, HTTPException
from database import LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from schemas import UserValidation











router=APIRouter(
    prefix="/auth",
    tags=["AUTH LOGIC"]
) 



def database_dependency():
    db=LocalSession()
    try:
        yield db 
    finally:
        db.close()

db_inj=Annotated[Session, Depends(database_dependency)]






@router.get("/reading-all-the-users")
async def All_users(db:db_inj):
    return db.query(Users).all()



@router.post("/adding-users")
async def Add_new_user(db:db_inj, new_user:UserValidation):

    model=Users(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        username =new_user.username,
        email=new_user.email,
        hashed_password=new_user.password,
        role=new_user.role,
        is_active=new_user.is_active
    )
    
    return model 
####### starts from here 





