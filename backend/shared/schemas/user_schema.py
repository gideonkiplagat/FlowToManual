# backend/shared/schemas/user_schema.py
from pydantic import BaseModel
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str
    password: str
    role: str

class UserLoginSchema(BaseModel):
    username: str
    password: str