from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class registerSchema(BaseModel):
    name: str
    password: str = Field(min_length=6)
    email: EmailStr


class loginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class exerciseSchema(BaseModel):
    email: EmailStr
    count: int
    calories: float
    exercise: str
    date: datetime
    weight: float
