from database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship




class Users(Base):
    __tablename__="users_data"

    id =Column(Integer, primary_key=True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    username =Column(String, unique=True)
    email=Column(String, unique=True )
    hashed_password=Column(String)
    role =Column(String)
    phone=Column(String, unique=True)
    is_active=Column(Boolean, default=True)


class Inventory(Base):

    __tablename__="inventory_data"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    type=Column(String)
    description=Column(String)
    sku=Column(String)
    stock=Column(Boolean)
    quantity=Column(Integer)
    price=Column(Integer)
    owner_id=Column(Integer, ForeignKey("users_data.id"))



class Messages(Base):

    __tablename__="user_messages"

    id =Column(Integer, primary_key=True, index=True)
    title =Column(String)
    description=Column(String)
    user_username =Column(String, ForeignKey("users_data.username"))
    user_email =Column(String, ForeignKey("users_data.email"))
    status=Column(String)

    # user=relationship(Users,backref="messages")
    















