from fastapi import APIRouter, Depends, HTTPException
from database import LocalSession
from sqlalchemy.orm import Session
from typing import Annotated
from models import Users
from .auth import get_current_user
from schemas import ChangePasswordValidation
from starlette import status
from passlib.context import CryptContext







router=APIRouter(
    prefix="/user/setting",
    tags=["USERS SETTING"]
)




def database_dependency():
    db=LocalSession()
    try:
        yield db 
    finally:
        db.close()


db_inj=Annotated[Session, Depends(database_dependency)]
user_inj=Annotated[dict, Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.put("/change-password/{old_password}/", status_code=status.HTTP_204_NO_CONTENT)
async def Changing_the_password(user:user_inj, db:db_inj, old_password:str , new_password:ChangePasswordValidation):

    if user is None or user.get("role")=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SORRY USER DOES NOT EXIST OR ADMINS ARE NOT ALLOWED")
    
    model =db.query(Users).filter(Users.id==user.get("id")).first()

    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID VERIFICATION FAILED")
    
    old_password_verification=bcrypt_context.verify(old_password, model.hashed_password)
    old_and_new_verification=bcrypt_context.verify(new_password.password, model.hashed_password)

    if not old_password_verification or old_and_new_verification:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOUR OLD PASSWORD VERIFICATION FAILED OR BOTH PASSWORDS ARE SAME")

    model.hashed_password=bcrypt_context.hash(new_password.password)

    db.add(model)
    db.commit()







