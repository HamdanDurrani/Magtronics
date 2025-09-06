from fastapi import FastAPI
import models 
from database import engine
from routes import magatronics, auth



app=FastAPI(
    title="MAGATRONICS",
    description="THIS IS THE BACK END OF MAGATRONICS WEBSITE WHERE WE PERFORM CRUD AND WE CAN HAVE DIFFERENT USERS "
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
# app.include_router(magatronics.router)

