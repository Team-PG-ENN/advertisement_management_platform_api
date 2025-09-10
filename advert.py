from fastapi import FastAPI
from pydantic import BaseModel
from db import adverts_collection
from bson import ObjectId

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
    return {"message": "Welcome to Grow_c6 advertisement management platform"}

# add advevrt endpoint
@app.post("/add_advert")
def add_advert(advert: Adverts):
    result = adverts_collection.insert_one(advert.dict())
    return {"message": "Advert added successfully", "id": str(result.inserted_id)}

# view advert endpoint
@app.get("/view_advert")
def view_advert():
    adverts = list(adverts_collection.find({}))
    for advert in adverts:
        advert["id"] = str(advert["_id"])
        del advert["_id"]
    return {"adverts": adverts}


# find advert endpoint
@app.get("/find_advert/{id_or_title}")
def find_advert(id_or_title: str):
    try:
        object_id = ObjectId(id_or_title)
        advert = adverts_collection.find_one({"_id": object_id})
        advert["id"] = str(advert["_id"])
        del advert["_id"]
        return {"advert": advert}
    except:
        adverts = list(adverts_collection.find({"Title": {"$regex": id_or_title, "$options": "i"}}))
        for advert in adverts:
            advert["id"] = str(advert["_id"])
            del advert["_id"]
        return {"message": "Advert not found"}
    

# delete endpint
@app.delete("/delete_advert/{id}")
def delete_advert(id: str):
    try:
        object_id = ObjectId(id)
        adverts_collection.delete_one({"_id": object_id})
        return {"message": "Advert deleted successfully"}
    except:
        return {"message": "Invalid ID format"}


# update endpoint
@app.put("/update_advert/{id}")
def update_advert(id: str, advert: Adverts):
    try:
        object_id = ObjectId(id)
        result = adverts_collection.update_one({"_id": object_id}, {"$set": advert.dict()})
        return {"message": "Advert updated successfully"} if result.matched_count else {"message": "Data not found"}
    except:
        return {"message": "Invalid ID format"}