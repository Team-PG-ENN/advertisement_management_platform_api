# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from db import adverts_collection
# from bson import ObjectId
# from bson.errors import InvalidId


# class Advert(BaseModel):
#     job_title: str
#     job_description: str
#     category: str
#     salaries: float


# app = FastAPI()


# # endpoint for advert management
# # User Flow
# @app.get("/", tags=["Home"])
# def home_page():
#     return {"message": "Welcome to XXXXXXXXX advertisement management platform"}


# # add job advert endpoint
# @app.post("/add_advert")
# def add_job(advert: Advert):
#     try:
#         result = adverts_collection.insert_one(advert.dict())
#         return {"message": "Advert added successfully", "job_id": str(result.inserted_id)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # view all available jobs endpoint
# @app.get("/view_advert")
# def view_advert():
#     try:
#         jobs = list(adverts_collection.find())
#         jobs_list = []
#         for job in jobs:
#             job["_id"] = str(job["_id"])
#             jobs_list.append(job)
#         return {"adverts": jobs_list}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # find job advert endpoint
# @app.get("/find_job/{find_job}")
# def find_job(find_job: str):
#     try:
#         if find_job.isdigit():
#             advert = adverts_collection.find_one({"_id": ObjectId(find_job)})
#             if advert:
#                 advert["_id"] = str(advert["_id"])
#                 return {"advert": advert}
#             else:
#                 return {"message": "Job not found"}
#         else:
#             advert = adverts_collection.find({"$or": [{"job_title": {"$regex": find_job, "$options": "i"}}, {"category": {"$regex": find_job, "$options": "i"}}, {"job_description": {"$regex": find_job, "$options": "i"}}]})
#             adverts = list(advert)
#             if adverts:
#                 for advert in adverts:
#                     advert["_id"] = str(advert["_id"])
#                 return {"adverts": adverts}
#             else:
#                 return {"message": "No jobs found"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# # delete job advert endpoint
# @app.delete("/delete_job/{job_id}")
# def delete_job(job_id: str):
#     try:
#         result = adverts_collection.delete_one({"_id": ObjectId(job_id)})
#         if result.deleted_count:
#             return {"message": "Job advert deleted successfully"}
#         else:
#             raise HTTPException(status_code=404, detail="Job advert not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # update job advert endpoint
# @app.put("/update_job/{job_id}")
# def update_job(job_id: str, advert: Advert):
#     try:
#         result = adverts_collection.update_one({"_id": ObjectId(job_id)}, {"$set": advert.dict()})
#         if result.modified_count:
#             return {"message": "Job advert updated successfully"}
#         else:
#             raise HTTPException(status_code=404, detail="Job advert not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from db import adverts_collection
# from bson import ObjectId

# class Advert(BaseModel):
#     job_title: str
#     job_description: str
#     category: str
#     salaries: float


# app = FastAPI()


# # endpoint for advert management
# # User Flow
# @app.get("/", tags=["Home"])
# def home_page():
#     return {"message": "Welcome to Grow_c6 advertisement management platform"}


# # add advevrt endpoint
# @app.post("/add_advert")
# def add_advert(advert: Adverts):
#     result = adverts_collection.insert_one(advert.dict())
#     return {"message": "Advert added successfully", "id": str(result.inserted_id)}

# # view advert endpoint
# @app.get("/view_advert")
# def view_advert():
#     adverts = list(adverts_collection.find({}))
#     for advert in adverts:
#         advert["id"] = str(advert["_id"])
#         del advert["_id"]
#     return {"adverts": adverts}


# # find advert endpoint
# @app.get("/find_advert/{id_or_title}")
# def find_advert(id_or_title: str):
#     try:
#         object_id = ObjectId(id_or_title)
#         advert = adverts_collection.find_one({"_id": object_id})
#         advert["id"] = str(advert["_id"])
#         del advert["_id"]
#         return {"advert": advert}
#     except:
#         adverts = list(adverts_collection.find({"Title": {"$regex": id_or_title, "$options": "i"}}))
#         for advert in adverts:
#             advert["id"] = str(advert["_id"])
#             del advert["_id"]
#         return {"message": "Advert not found"}
    

# # delete endpint
# @app.delete("/delete_advert/{id}")
# def delete_advert(id: str):
#     try:
#         object_id = ObjectId(id)
#         adverts_collection.delete_one({"_id": object_id})
#         return {"message": "Advert deleted successfully"}
#     except:
#         return {"message": "Invalid ID format"}


# # update endpoint
# @app.put("/update_advert/{id}")
# def update_advert(id: str, advert: Adverts):
#     try:
#         object_id = ObjectId(id)
#         result = adverts_collection.update_one({"_id": object_id}, {"$set": advert.dict()})
#         return {"message": "Advert updated successfully"} if result.matched_count else {"message": "Data not found"}
#     except:
#         return {"message": "Invalid ID format"}
=======
# add job advert endpoint


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import adverts_collection
from bson import ObjectId

class Advert(BaseModel):
    job_title: str
    job_description: str
    category: str
    salaries: float


app = FastAPI()

@app.post("/add_job")
def add_job(advert: Advert):
    try:
        result = adverts_collection.insert_one(advert.dict())
        return {"message": "Advert added successfully", "job_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# view all available jobs endpoint
@app.get("/view_job")
def view_job():
    try:
        jobs = list(adverts_collection.find())
        jobs_list = []
        for job in jobs:
            job["_id"] = str(job["_id"])
            jobs_list.append(job)
        return {"adverts": jobs_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# find job advert endpoint - FIXED VERSION
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
            # Invalid ObjectId, continue to text search
            pass
        
        # Search by text fields with partial matching
        query = {"$or": [
            {"job_title": {"$regex": find_job, "$options": "i"}},
            {"job_description": {"$regex": find_job, "$options": "i"}},
            {"category": {"$regex": find_job, "$options": "i"}}
        ]}
        
        cursor = adverts_collection.find(query)
        adverts = list(cursor)
        
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
