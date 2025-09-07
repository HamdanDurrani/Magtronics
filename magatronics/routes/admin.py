from fastapi import APIRouter, Depends, HTTPException
from database import LocalSession
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from models import Users, Inventory, Messages
from schemas import InventoryValidation, StatusValidation
from starlette import status


# ##########################################################################################################################################


router=APIRouter(
    prefix="/admin/admins-protected",
    tags=["ADMINS CRUD (only for admins)"]
)


# ##########################################################################################################################################

def database_dependency():
    db=LocalSession()
    try:
        yield db 
    finally:
        db.close()


db_inj=Annotated[Session, Depends(database_dependency)]
user_inj=Annotated[dict, Depends(get_current_user)]


# ##########################################################################################################################################


@router.get("/get-all-users", status_code=status.HTTP_200_OK)
async def Reading_all_users(user:user_inj, db:db_inj):

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    return db.query(Users).filter(Users.role=="user").all()



@router.get("/get-all-admins", status_code=status.HTTP_200_OK)
async def Reading_all_admins(user:user_inj, db:db_inj):


    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")
    return db.query(Users).filter(Users.role=="admin").all()


@router.get("/get-all-products", status_code=status.HTTP_200_OK)
async def Reading_all_products(user:user_inj, db:db_inj):

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    return db.query(Inventory).all()

@router.get("/read-user-messages", status_code=status.HTTP_200_OK)
async def Reading_all_messages_of_user(user:user_inj, db:db_inj):

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    return db.query(Messages).all()


@router.get("/read-user-messages/email-required/", status_code=status.HTTP_200_OK)
async def Reading_specific_messages_of_user(user:user_inj, db:db_inj, email:str):

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    model =db.query(Messages).filter(Messages.user_email==email).first()

    return {
        "title":model.title,
        "message":model.description,
        "username":model.user_username,
        "user-emaail":model.user_email,
        "status":model.status
    }


# ##########################################################################################################################################




@router.post("/add-a-product/adding/", status_code=status.HTTP_201_CREATED)
async def Adding_a_product(user:user_inj, db:db_inj, new_product:InventoryValidation):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    model = Inventory(**new_product.model_dump())

    db.add(model)
    db.commit()
    return "ADDED SUCESSFULLY"


# ##########################################################################################################################################


@router.put("/update-user-complaints/email-required/", status_code=status.HTTP_204_NO_CONTENT)
async def Update_complaint_status(user:user_inj, db:db_inj, email:str, updated_status:StatusValidation):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")

    model = db.query(Messages).filter(Messages.user_email==email).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR EMAIL NOT FOUND")
    
    model.status=updated_status.status
    db.add(model)
    db.commit()



@router.put("/updating-a-stock/update-type-required/id-required/{id}/{update_type}",status_code=status.HTTP_204_NO_CONTENT)
async def Edit(user:user_inj, db:db_inj, id:int , updated:InventoryValidation, update_type ):

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")
    
    model= db.query(Inventory).filter(Inventory.id == id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID DOES NOT EXIST")
    
    
    if update_type=="name":
        model.name =updated.name
    elif update_type=="type":
        model.type =updated.type
    elif update_type=="description":
        model.description=updated.description
    elif update_type=="sku":
        model.sku = updated.sku
    elif update_type=="stock":
        model.stock = updated.stock
    elif update_type=="quantity":
        model.quantity=updated.quantity
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR UPDATE TYPE NOT FOUND")

    db.add(model)
    db.commit()

# ##########################################################################################################################################

@router.delete("/out-of-stock/inventory-out-of-stock/id-required/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def Making_an_item_OUTOFSTOCK(user:user_inj, db:db_inj, id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")
    
    model = db.query(Inventory).filter(Inventory.id==id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID DOES NOT EXIST")
    
    model.stock=False

    db.add(model)
    db.commit()





@router.delete("/delete/delete-a-item-in-thr-inventory/id-required/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_a_item(user:user_inj, db:db_inj, id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="YOU USERNAME OR PASSWORD NOT FOUND")

    if user.get("role") == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT AN ADMIN")
    
    model = db.query(Inventory).filter(Inventory.id==id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID DOES NOT EXIST")
    
    model =db.query(Inventory).filter(Inventory.id==id).delete()
    db.commit()
