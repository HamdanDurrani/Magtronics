from pydantic import BaseModel, Field, field_validator
from typing import Optional





class TokenValidation(BaseModel):
    access_token: str
    token_type: str 




class UserValidation(BaseModel):

    first_name:str
    last_name:str
    username:str 
    email:str 
    password:str 
    phone:str
    role:Optional[str]="user" 
    is_active:Optional[bool]=True

    class Config:
        json_schema_extra={
            "example":{
                "first_name":"first",
                "last_name":"last",
                "username":"user",
                "email":"@gmail.com",
                "password":"xxxxxx",
                "phone":"0300-0000000"
            }
        }



class InventoryValidation(BaseModel):

    name:str
    type:str 
    description:str 
    sku:str 
    quantity:int
    stock:bool 
    price:int

    class Config:
        json_schema_extra={
            "example":{
                "name":"product_name",
                "type":"product_type",
                "description":"product_description",
                "sku":"123-xx0x",
                "stock":True,
                "quantity":0,
                "price":0
            }
        }



class MessageValidation(BaseModel):

    id:Optional[int]=250000
    title:str 
    description:str 
    # user_username:str #forgien key 
    # user_email:str    #forgien key 
    status:Optional[str]="JUST REQUESTED"

    class config:
        json_schema_extra={
            "example":{
                "title":"title_of _your_complaint",
                "description":"Describe_your_complaint",
            }
        }


class StatusValidation(BaseModel):

    status:Optional[str]="SEEN JUST NOW"

    class Config:
        json_schema_extra={
            "example":{
                "status":"AS AN AMDIM ENTER YOUR REMARKS"
            }
        }



class ChangePasswordValidation(BaseModel):

    password:str=Field(min_length=8)

    class Config:
        json_schema_extra={
            "example":{
                "password":"XXX-MUST_BE_8_DIGITS-XXX"
            }
        }

    # @field_validator
    # def password_request()

