from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class registerSchema(BaseModel):
    name: str
    password: str = Field(min_length=6)
    email: str


class loginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class exerciseSchema(BaseModel):
    userID: str
    count: int
    calories: float
    exercise: str
    date: datetime
