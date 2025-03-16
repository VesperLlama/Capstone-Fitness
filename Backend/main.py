from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.userModel import registerSchema, loginSchema, exerciseSchema
from bson.json_util import dumps
from CV_models.dumbell_curl import process_frame as dumbbell
from CV_models.Shoulderpress import process_frame as shldpress
from CV_models.Push_Up_Counter import process_frame as pushUpCount

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.getenv("DB_URL"))
db = client["fitfusion"]
users = db["users"]
exData = db["exData"]
secret = os.getenv("key")


@app.post("/register")
def register(data: registerSchema) -> Response:
    print(data)
    existing_user = users.find_one({"email": data.email}, {"_id": 0})
    if existing_user:
        return JSONResponse(content={"message": "Email already exists"})

    users.insert_one(data.dict())
    return JSONResponse(content={"message": "Account created successfully!"})


@app.post("/login")
def login(data: loginSchema):
    user = users.find_one({"email": data.email, "password": data.password})
    if not user:
        return JSONResponse(content={"message": "User does not exist."})
    else:
        token = jwt.encode({"Email": data.email}, secret, algorithm="HS256")
        return JSONResponse(
            content={
                "message": "Logged in successfully!",
                "token": token,
                "email": data.email,
            }
        )


@app.post("/addData")
async def addData(data: exerciseSchema):
    userID = users.find_one({"email": data.email})
    data = data.dict()
    data["userID"] = str(userID.get("_id"))
    del data["email"]
    result = exData.insert_one(data)
    return JSONResponse(content={"message": "Success"})


@app.get("/getData/{email}")
async def getData(email):
    getOiD = users.find_one({"email": email})
    data = exData.find({"userID": str(getOiD.get("_id"))})
    data = list(data)
    return dumps(data)


@app.post("/cv/dumbell")
async def dumbell(file: UploadFile = File(...)):
    contents = await file.read()
    img_str, count = dumbbell(contents)
    return JSONResponse(
        content={"image": f"data:image/jpeg;base64,{img_str}", "count": count}
    )


@app.post("/cv/shldpress")
async def shoulderPress(file: UploadFile = File(...)):
    contents = await file.read()
    img_str, count = shldpress(contents)
    return JSONResponse(
        content={"image": f"data:image/jpeg;base64,{img_str}", "count": count}
    )


@app.post("/cv/pushup")
async def pushUp(file: UploadFile = File(...)):
    contents = await file.read()
    img_str, count = pushUpCount(contents)
    return JSONResponse(
        content={"image": f"data:image/jpeg;base64,{img_str}", "count": count}
    )
