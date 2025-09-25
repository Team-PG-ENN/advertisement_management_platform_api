from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from bson.errors import InvalidId
from db import adverts_collection
from typing import List
from datetime import date

app = FastAPI()

class Advert(BaseModel):
    job_title: str
    job_description: str
    category: str
    salaries: float
    image: str
    skills: List[str]
    created_at: str = Field(default_factory=lambda: date.today().isoformat())


@app.post("/add_job")
def add_job(advert: Advert):
    try:
        result = adverts_collection.insert_one(advert.dict())
        return {"message": "Advert added successfully", "job_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view_job")
def view_job():
    try:
        jobs = list(adverts_collection.find())
        for job in jobs:
            job["_id"] = str(job["_id"])
        return {"adverts": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/find_job/{find_job}")
def find_job(find_job: str):
    try:
        # Try to find by ObjectId first
        try:
            advert = adverts_collection.find_one({"_id": ObjectId(find_job)})
            if advert:
                advert["_id"] = str(advert["_id"])
                return {"advert": advert}
        except (InvalidId, ValueError):
            pass

        # Search by text fields with partial matching
        query = {"$or": [
            {"job_title": {"$regex": find_job, "$options": "i"}},
            {"job_description": {"$regex": find_job, "$options": "i"}},
            {"category": {"$regex": find_job, "$options": "i"}}
        ]}
        
        adverts = list(adverts_collection.find(query))
        
        if adverts:
            for advert in adverts:
                advert["_id"] = str(advert["_id"])
            return {"adverts": adverts}

        return {"message": "No jobs found"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete job advert endpoint
@app.delete("/delete_job/{job_id}")
def delete_job(job_id: str):
    try:
        result = adverts_collection.delete_one({"_id": ObjectId(job_id)})
        if result.deleted_count:
            return {"message": "Job advert deleted successfully"}
        return {"message": "Job advert not found"}
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# update job advert endpoint
@app.put("/update_job/{job_id}")
def update_job(job_id: str, advert: Advert):
    try:
        result = adverts_collection.update_one({"_id": ObjectId(job_id)}, {"$set": advert.dict()})
        if result.modified_count:
            return {"message": "Job advert updated successfully"}
        return {"message": "Job advert not found or no changes made"}
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




