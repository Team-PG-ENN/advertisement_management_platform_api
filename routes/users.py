from enum import Enum
from fastapi import APIRouter, Form, HTTPException, status
from db import users_collection
from typing import Annotated
from pydantic import EmailStr
import bcrypt
import jwt
import os
from datetime import datetime, timezone, timedelta


# create vendor router
users_router = APIRouter()


class UserRole(str, Enum):
    ADMIN = "admin"
    COMPANY = "company"
    USER = "user"


# register as company (vendor)
@users_router.post("/users/register", tags=["Users"])
def register_user(
    user_name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    role: Annotated[UserRole, Form()] = UserRole.USER,
):
    # ensure company (vendor) does not already exist
    user = users_collection.find_one(filter={"email": email})
    if user:
        raise HTTPException(status.HTTP_409_CONFLICT, "user already exist")
    # Hash company password (vendor)
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # save company into data (vendor)
    user = users_collection.insert_one(
        {"user name": user_name, "email": email, "password": hash_password, "role": role}
    )
    # return register succesfull (vendor)
    return {"message": "user registered successfully"}


# login as vendor
# log in as company (vendor)
@users_router.post("/users/login", tags=["Users"])
def login_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    role: Annotated[UserRole, Form()] =  UserRole.USER, 
):
    # ensure user exist by finding them in the database using the email as a filter
    user = users_collection.find_one(filter={"email": email})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user does not exist")

    # compare the password
    correct_password = bcrypt.checkpw(password.encode(), user["password"])
    if not correct_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    # generate an access token for them
    encoded_jwt = jwt.encode(
        {
            "id": str(user["_id"]),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=600),
        },
        key=os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256",
    )

    # return response

    return {"message": "User logged in successfully!", "access_token": encoded_jwt}
