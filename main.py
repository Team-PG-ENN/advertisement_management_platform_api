from fastapi import FastAPI
from dotenv import load_dotenv
from routes.users import users_router
from routes.adverts import adverts_router
import os
import cloudinary


load_dotenv()

#configure cloudinary
cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET")
)

app = FastAPI(title= "SkillBridge Advertisement App", description= "You are welcome, find your dream Jobs")
@app.get("/", tags=["Home"])
def home_page():
    return {"message": "Welcome to SkillBridge advertisement management platform"}


#include routers
app.include_router(users_router)
app.include_router(adverts_router)





