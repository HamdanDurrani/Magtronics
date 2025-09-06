from pydantic import BaseModel
from typing import Optional






class InventoryValidation(BaseModel):

    name:str
    type:str 
    description:str 
    sku:str 
    stock:bool 



class UserValidation(BaseModel):

    first_name:str
    last_name:str
    username:str 
    email:str 
    password:str 
    role:Optional[str]="user" 
    is_active:Optional[bool]=True

    class Config:
        json_schema_extra={
            "example":{
                "first_name":"first",
                "last_name":"last",
                "username":"user",
                "email":"@gmail.com",
                "password":"xxxxxx"
            }
        }











