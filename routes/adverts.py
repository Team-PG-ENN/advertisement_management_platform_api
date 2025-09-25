from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from db import adverts_collection
from bson import ObjectId
from bson.errors import InvalidId
from typing import Annotated
from datetime import date
from dependencies.authz import has_roles
import cloudinary
import cloudinary.uploader




adverts_router = APIRouter()


class Advert(BaseModel):
    job_title: str
    job_description: str
    category: str
    salaries: str
    skills: str
    created_at: str = Field(default_factory=lambda: date.today().isoformat())


# add advert endpoint
@adverts_router.post(
    "/add_job", dependencies=[Depends(has_roles("company"))], tags=["Adverts"]
)
def add_job(advert: Advert, flyer: Annotated[UploadFile, File()]):
    # Check if advert already exists
    advert_count = adverts_collection.count_documents({
        "$and": [
            {"job_title": advert.job_title},
            {"job_description": advert.job_description}
        ]
    })

    if advert_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An advert with job title'{advert.job_title}' already exists."
        )

    try:
        # Upload flyer to cloudinary and get secure URL
        upload_result = cloudinary.uploader.upload(flyer.file)
        flyer_url = upload_result["secure_url"]

        # Merge flyer URL into advert data
        advert_data = advert.model_dump()
        advert_data["flyer"] = flyer_url

        # Insert advert into collection
        result = adverts_collection.insert_one(advert_data)

        return {
            "message": "Advert added successfully",
            "job_id": str(result.inserted_id),
            "flyer_url": flyer_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# view all advert endpoint
@adverts_router.get(
    "/job", dependencies=[Depends(has_roles("recruiter"))], tags=["Adverts"]
)
def view_all_job():
    try:
        jobs = list(adverts_collection.find())
        for job in jobs:
            job["_id"] = str(job["_id"])
        return {"adverts": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# find a single job advert 
@adverts_router.get("/find_job/{find_job}", tags=["Adverts"])
def find_job(job_title="", job_description="", limit=10, skip=0):
    advert = adverts_collection.find_one(
        filter={
            "$or": [
                {"title": {"$regex": job_title, "$options": "i"}},
                {"description": {"$regex": job_description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    )
    if advert:
        return {"advert": advert}
    else:
        return {"message": "No jobs found"}


# delete job advert endpoint
@adverts_router.delete(
    "/advert/{job_id}", dependencies=[Depends(has_roles("company"))], tags=["Adverts"])
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
@adverts_router.put(
    "/advert/{job_id}", dependencies=[Depends(has_roles("company"))], tags=["Adverts"]
)
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