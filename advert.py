from fastapi import FastAPI
from pydantic import BaseModel
from db import adverts_collection


class Adverts(BaseModel):
    Title: str
    Description: str
    Category: str
    Price: float


app = FastAPI()


# endpoint for advert management
# User Flow
@app.get("/", tags=["Home"])
def home_page():
    return {"message": "Welcome to XXXXXXXXX advertisement management platform"}


# add advevrt endpoint
@app.post("/add_advert")
def add_advert(adverts: Adverts):
    adverts_collection.insert_one(adverts.dict())
    return {"message": "Advert added successfully"}



# view advert endpoint
@app.get("/view_advert")
def view_advert():
    adverts = list(adverts_collection.find({}, {"_id": 0}))
    return {"adverts": adverts}


# find advert endpoint
@app.get("/find_advert/{title}")
def find_advert(title: str):
    advert = adverts_collection.find_one({"Title": title}, {"_id": 0})
    if advert:
        return {"advert": advert}
    else:
        return {"message": "Advert not found"}


# delete advert endpoint
@app.delete("/delete_advert/{title}")
def delete_advert(title: str):
    result = adverts_collection.delete_one({"Title": title})
    if result.deleted_count:
        return {"message": "Advert deleted successfully"}
    else:
        return {"message": "Advert not found"}


# update advert endpoint
@app.put("/update_advert/{title}")
def update_advert(title: str, adverts: Adverts):
    result = adverts_collection.update_one({"Title": title}, {"$set": adverts.dict()})
    if result.modified_count:
        return {"message": "Advert updated successfully"}
    else:
        return {"message": "Advert not found or no changes made"}
