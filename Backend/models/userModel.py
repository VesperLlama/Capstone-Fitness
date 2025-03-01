from pydantic import BaseModel, Field, EmailStr


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
    exercise: str
