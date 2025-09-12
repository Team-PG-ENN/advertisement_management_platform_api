
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



# from fastapi import FastAPI, HTTPException, File, UploadFile
# from pydantic import BaseModel, Field
# from bson import ObjectId
# from bson.errors import InvalidId
# from db import adverts_collection
# from typing import List
# from datetime import date
# import cloudinary
# import cloudinary.uploader
# import os

# app = FastAPI()


# # Cloudinary configuration
# cloudinary.config(
#     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.getenv("CLOUDINARY_API_KEY"),
#     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# )

# # Pydantic model for job advert data
# class Advert(BaseModel):
#     job_title: str
#     job_description: str
#     category: str
#     salaries: float
#     image: str  # Stores the Cloudinary URL of the uploaded image
#     skills: List[str]
#     created_at: str = Field(default_factory=lambda: date.today().isoformat())

# # Endpoint to add a new job advert with image upload
# @app.post("/add_job")
# async def add_job(
#     job_title: str,
#     job_description: str,
#     category: str,
#     salaries: float,
#     skills: str,  # Comma-separated string of skills
#     image: UploadFile = File(...)
# ):
#     try:
#         # Upload image to Cloudinary
#         upload_result = cloudinary.uploader.upload(image.file)
#         image_url = upload_result.get("url")

#         # Parse skills from comma-separated string
#         skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]

#         # Create Advert instance
#         advert = Advert(
#             job_title=job_title,
#             job_description=job_description,
#             category=category,
#             salaries=salaries,
#             image=image_url,
#             skills=skills_list
#         )

#         # Insert into MongoDB
#         result = adverts_collection.insert_one(advert.dict())
#         return {"message": "Advert added successfully", "job_id": str(result.inserted_id)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to view all job adverts
# @app.get("/view_job")
# async def view_job():
#     try:
#         jobs = list(adverts_collection.find())
#         for job in jobs:
#             job["_id"] = str(job["_id"])
#         return {"adverts": jobs}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to find job adverts by ID or text search
# @app.get("/find_job/{find_job}")
# async def find_job(find_job: str):
#     try:
#         # Try to find by ObjectId first
#         try:
#             advert = adverts_collection.find_one({"_id": ObjectId(find_job)})
#             if advert:
#                 advert["_id"] = str(advert["_id"])
#                 return {"advert": advert}
#         except (InvalidId, ValueError):
#             pass

#         # Search by text fields with partial matching
#         query = {"$or": [
#             {"job_title": {"$regex": find_job, "$options": "i"}},
#             {"job_description": {"$regex": find_job, "$options": "i"}},
#             {"category": {"$regex": find_job, "$options": "i"}}
#         ]}
        
#         adverts = list(adverts_collection.find(query))
        
#         if adverts:
#             for advert in adverts:
#                 advert["_id"] = str(advert["_id"])
#             return {"adverts": adverts}

#         return {"message": "No jobs found"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to delete a job advert by ID
# @app.delete("/delete_job/{job_id}")
# async def delete_job(job_id: str):
#     try:
#         result = adverts_collection.delete_one({"_id": ObjectId(job_id)})
#         if result.deleted_count:
#             return {"message": "Job advert deleted successfully"}
#         return {"message": "Job advert not found"}
#     except InvalidId:
#         raise HTTPException(status_code=400, detail="Invalid ObjectId format")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to update a job advert by ID
# @app.put("/update_job/{job_id}")
# async def update_job(
#     job_id: str,
#     job_title: str,
#     job_description: str,
#     category: str,
#     salaries: float,
#     skills: str,
#     image: UploadFile = File(None)  # Image is optional for updates
# ):
#     try:
#         # Parse skills from comma-separated string
#         skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]

#         # Prepare update data
#         update_data = {
#             "job_title": job_title,
#             "job_description": job_description,
#             "category": category,
#             "salaries": salaries,
#             "skills": skills_list,
#             "created_at": date.today().isoformat()
#         }

#         # Handle image update if provided
#         if image:
#             # Upload image to Cloudinary
#             upload_result = cloudinary.uploader.upload(image.file)
#             image_url = upload_result.get("url")
#             update_data["image"] = image_url

#         # Update in MongoDB
#         result = adverts_collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})
#         if result.modified_count:
#             return {"message": "Job advert updated successfully"}
#         return {"message": "Job advert not found or no changes made"}
#     except InvalidId:
#         raise HTTPException(status_code=400, detail="Invalid ObjectId format")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
