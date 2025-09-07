from fastapi import APIRouter, Depends, HTTPException
from database import LocalSession
from typing import Annotated
from sqlalchemy.orm import Session,session
from models import Users
from schemas import UserValidation, TokenValidation
from passlib.context import CryptContext 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError

# ##########################################################################################################################################


router=APIRouter(
    prefix="/auth",
    tags=["AUTH LOGIC"]
) 



bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
form_inj=Annotated[OAuth2PasswordRequestForm, Depends()]
SECERT_KEY="4152fd00ede97585f02a65d56a8986a200c7dcf99ec91292fb036471e5d28f91"
ALGORITHM="HS256"
JSON_EXPIRE_TIME:timedelta=timedelta(minutes=20)
oauth2=OAuth2PasswordBearer(tokenUrl="/auth/token")

# ##########################################################################################################################################


def database_dependency():
    db=LocalSession()
    try:
        yield db 
    finally:
        db.close()


db_inj=Annotated[Session, Depends(database_dependency)]

def authenticate_a_user(username:str, password:str, db):

    model = db.query(Users).filter(Users.username==username).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOUR USERNAME IS INVALID")
    
    model_password_check=model.hashed_password
    password_verification=bcrypt_context.verify(password, model_password_check)
    if not password_verification:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOUR PASSWORD IS INVALID")
    
    return model

def create_access_token(username:str, id :int, role:str, exp_time:timedelta):
    encode={
        "sub":username,
        "id":id,
        "role":role
    }
    e_time =datetime.now(timezone.utc) + exp_time
    encode.update({"exp":e_time})

    return jwt.encode(encode, key=SECERT_KEY, algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str, Depends(oauth2)]):

    try:
        payload =jwt.decode(token, key=SECERT_KEY, algorithms=ALGORITHM)
        username:str = payload.get("sub")
        id:int=payload.get("id")
        role:str= payload.get("role")

        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOUR ID OR USERNAME IS NONE")
        
        return {
            "username":username,
            "id":id,
            "role":role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="THERE IS ERROR IN YOUR JWT")
    


# ##########################################################################################################################################



@router.get("/reading-all-the-users", status_code=status.HTTP_200_OK)
async def All_users(db:db_inj):
    return db.query(Users).all()


# ##########################################################################################################################################


#role     =  user |  admin

#username =    a  |  hamdan
#password =    a  |  hamdan



@router.post("/adding-users", status_code=status.HTTP_201_CREATED)
async def Add_new_user(db:db_inj, new_user:UserValidation):

    model=Users(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        username =new_user.username,
        email=new_user.email,
        hashed_password=bcrypt_context.hash(new_user.password),
        role=new_user.role,
        is_active=new_user.is_active,
        phone=new_user.phone
    )

    username_check= db.query(Users).filter(Users.username==model.username).first()
    if username_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="USERNAME ALREADY EXIST")
    email_check=db.query(Users).filter(Users.email==model.email).first()
    if email_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EMAIL ALREADY EXIST GO AND LOG IN ")
    phone_check=db.query(Users).filter(Users.phone==model.phone).first()
    if phone_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOUR PHONE NUMBER IS ALREADY REGISTERED")

    db.add(model)
    db.commit()
    return "YOUR USER IS ADDEDD SUCESSFULLY"



# ##########################################################################################################################################

@router.post("/token",response_model=TokenValidation, status_code=status.HTTP_201_CREATED)
async def Access_token(form:form_inj, db:db_inj):

    model=authenticate_a_user(form.username, form.password, db=db )

    token=create_access_token(model.username, model.id, model.role, JSON_EXPIRE_TIME)

    return {"access_token":token,"token_type":"bearer"}

