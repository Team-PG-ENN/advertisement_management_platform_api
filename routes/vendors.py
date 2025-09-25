from enum import Enum
from fastapi import APIRouter, Form, HTTPException, status
from db import vendors_collection
from typing import Annotated
from pydantic import EmailStr
import bcrypt
import jwt
import os
from datetime import datetime, timezone, timedelta


# create vendor router
vendors_router = APIRouter()


class UserRole(str, Enum):
    COMPANY = "company"
    RECRUITER = "recruiter"


# register as company (vendor)
@vendors_router.post("/vendors/register", tags=["Vendors"])
def register_vendor(
    vendor_name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    role: Annotated[UserRole, Form()] = UserRole.RECRUITER,
):
    # ensure company (vendor) does not already exist
    vendor = vendors_collection.find_one(filter={"email": email})
    if vendor:
        raise HTTPException(status.HTTP_409_CONFLICT, "vendor already exist")
    # Hash company password (vendor)
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # save company into data (vendor)
    vendor = vendors_collection.insert_one(
        {"vendor name": vendor_name, "email": email, "password": hash_password}
    )
    # return register succesfull (vendor)
    return {"message": "vendor registered successfully"}


# login as vendor
# log in as company (vendor)
@vendors_router.post("/vendors/login", tags=["Vendors"])
def login_vendor(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    role: Annotated[UserRole, Form()] =  UserRole.RECRUITER,
):
    # ensure user exist by finding them in the database using the email as a filter
    vendor = vendors_collection.find_one(filter={"email": email})
    if not vendor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "vendor does not exist")

    # compare the password
    correct_password = bcrypt.checkpw(password.encode(), vendor["password"])
    if not correct_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    # generate an access token for them
    encoded_jwt = jwt.encode(
        {
            "id": str(vendor["_id"]),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
        },
        key=os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256",
    )

    # return response

    return {"message": "Vendor logged in successfully!", "access_token": encoded_jwt}
