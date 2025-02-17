from pydantic import BaseModel, Field, EmailStr


class registerSchema(BaseModel):
    name: str
    password: str = Field(min_length=8)
    email: EmailStr
    mobileNo: str = Field(min_length=10, max_length=10)


class loginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class exerciseSchema(BaseModel):
    userID: str
    count: int
    exercise: str
