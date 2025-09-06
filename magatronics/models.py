from database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey





class Users(Base):
    __tablename__="users_data"

    id =Column(Integer, primary_key=True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    username =Column(String, unique=True)
    email=Column(String, unique=True )
    hashed_password=Column(String)
    role =Column(String)
    is_active=Column(Boolean, default=True)


class Inventory(Base):

    __tablename__="inventory_data"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    type=Column(String)
    description=Column(String)
    sku=Column(String)
    stock=Column(Boolean)
    owner_id=Column(Integer, ForeignKey("users_data.id"))
















