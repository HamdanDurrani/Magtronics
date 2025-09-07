from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import  LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import Inventory
from schemas import InventoryValidation
from .auth import get_current_user


router=APIRouter(
    prefix="/magatronics",
    tags=["MAIN CRUD "]
)




def database_dependency():
    db=LocalSession()
    try:
        yield db 
    finally:
        db.close()

db_inj=Annotated[Session, Depends(database_dependency)]
user_inj=Annotated[dict, Depends(get_current_user)]



@router.get("/read-all")
async def Read_all__items(user:user_inj, db:db_inj):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")  
    return db.query(Inventory).all()



@router.post("/adding-item")
async def Adding_an_item(db:db_inj, new_item:InventoryValidation):

    model = Inventory(**new_item.model_dump())

    db.add(model)
    db.commit()
    return "item added sucessfully" 



@router.put("/coustomizing-coustom/is-required/")
async def Edit(db:db_inj, id:int , updated:InventoryValidation):

    model= db.query(Inventory).filter(Inventory.id == id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID DOES NOT EXIST")
    
    model.name =updated.name
    model.type =updated.type
    model.description=updated.description
    model.sku = updated.sku
    model.stock = updated.stock

    db.add(model)
    db.commit()




@router.delete("/deleting/deletin-a-product/id-required/{id}")
async def Remove_an_item(db:db_inj, id :int):

    model =db.query(Inventory).filter(Inventory.id==id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="YOUR ID IS INVALID")
    
    model = db.query(Inventory).filter(Inventory.id==id).delete()

    db.commit()









