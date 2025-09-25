from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from db import adverts_collection
from utils import replace_mongo_id
from bson import ObjectId
from typing import Annotated
from dependencies.authn import is_authenticated
from dependencies.authz import has_roles
import cloudinary
import cloudinary.uploader


adverts_router = APIRouter()


# add advert endpoint
@adverts_router.post(
    "/add_job", dependencies=[Depends(has_roles("company"))], tags=["Adverts"]
)
def post_job(
    job_title: Annotated[str, Form()],
    job_description: Annotated[str, Form()],
    category: Annotated[str, Form()],
    salaries: Annotated[float, Form()],
    skills: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    user_id: Annotated[str, Depends(is_authenticated)],
     
):
    # Check if advert already exists
    advert_count = adverts_collection.count_documents(
        {
            "$and": [
                {"job_title": job_title},
                {"job_description": job_description},
                {"owner": ObjectId(user_id)},
            ]
        }
    )

    if advert_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Advert with {job_title}  and {user_id} already exist.",
        )
    # Upload flyer to cloudinary and get secure URL
    upload_result = cloudinary.uploader.upload(flyer.file)
    print(upload_result)
    # Insert advert into collection
    adverts_collection.insert_one(
        {
            "job_title": job_title,
            "job_description": job_description,
            "category": category,
            "salaries": salaries,
            "skills": skills,
            "flyer": upload_result["secure_url"],
            "owner": user_id,
        }
    )

    return {
        "message": "Advert added successfully",
        "owner": user_id,
        "flyer": upload_result
    }


# view all advert endpoint
@adverts_router.get(
    "/job", tags=["Adverts"]
)
def view_all_jobs(job_title="", job_description="", category="", limit=10, skip=0):
    # Get all advert from database
    adverts = adverts_collection.find(
        filter={
            "$or": [
                {"job_title": {"$regex": job_title, "$options": "i"}},
                {"job_description": {"$regex": job_description, "$options": "i"}},
                {"category": {"$regex": category, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()
    # Return response
    return {"data": list(map(replace_mongo_id, adverts))}


# find a single job advert
@adverts_router.get("/find_job/{find_job}", tags=["Adverts"])
def find_job(job_title="", job_description="", category="", limit=10, skip=0):
    advert = adverts_collection.find_one(
        filter={
            "$or": [
                {"title": {"$regex": job_title, "$options": "i"}},
                {"description": {"$regex": job_description, "$options": "i"}},
                {"category": {"$regex": category, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    )
    if advert:
        return {"advert": advert}
    else:
        return {"message": "No jobs found"}


@adverts_router.get("/jobs/{job_id}/similar", tags=["Adverts"])
def get_similar_jobs(job_id: str, limit: int = 10, skip: int = 0):
    # Validate job_id
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid MongoDB ObjectId received!"
        )
    # Get the reference job
    advert = adverts_collection.find_one({"_id": ObjectId(job_id)})
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job advert not found!"
        )

    # Find similar jobs based on category (and optionally skills)
    similar_adverts_cursor = adverts_collection.find(
        filter={
            "$or": [
                {"category": {"$regex": advert.get("category", ""), "$options": "i"}},
                {"_id": {"$ne": ObjectId(job_id)}},  # Exclude the original job
            ]
        },
        limit=int(limit),
        skip=int(skip),
    )

    # Convert cursor to list with Mongo _id replaced
    similar_adverts = list(map(replace_mongo_id, similar_adverts_cursor))

    return {"data": similar_adverts, "count": len(similar_adverts)}





# delete job advert endpoint
@adverts_router.delete(
    "/advert/{job_id}",
    dependencies=[Depends(has_roles("company"))], tags=["Adverts"]
)
def delete_job(job_id, user_id: Annotated[str, Depends(is_authenticated)]):
    # check if event_id id valid in mongo id
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "invalid mongo id recieved!"
        )
        # delete event from database
    delete_result = adverts_collection.delete_one(filter={"_id": ObjectId(job_id)})
    if not delete_result.deleted_count:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No event found to delete")
    #return response    
    return {"message": "event deleted successfully"}


# update job advert endpoint
@adverts_router.put(
    "/advert/{job_id}", dependencies=[Depends(has_roles("company"))], tags=["Adverts"]
)
def update_job(
    job_id,
    job_title: Annotated[str, Form()],
    job_description: Annotated[str, Form()],
    category: Annotated[str, Form()],
    salaries: Annotated[float, Form()],
    skills: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    user_id: Annotated[str, Depends(is_authenticated)],
    # created_at: str = Field(default_factory=lambda: date.today().isoformat()),
):
    # check if event_id is valid mongo id
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "invalid mongo id recieved!"
        )
      # upload flyer to cloudinary
    upload_result = cloudinary.uploader.upload(flyer.file)
    # replace event in database
    adverts_collection.replace_one(
        filter={"_id": ObjectId(job_id)},
        replacement=(
            {
            "job_title": job_title,
            "job_description": job_description,
            "category": category,
            "salaries": salaries,
            "skills": skills,
            "flyer": upload_result["secure_url"],
            "owner": user_id,
            }
        ),
    )
    return {"message": "Advert replaced successfully"}

    
