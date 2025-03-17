from fastapi import FastAPI, File, UploadFile, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
import os
import base64
from dotenv import load_dotenv
from pymongo import MongoClient
from models.userModel import registerSchema, loginSchema, exerciseSchema
from bson.json_util import dumps
from CV_models.dumbell_curl import process_frame as dumbbellExercise
from CV_models.Shoulderpress import process_frame as shldpressExercise
from CV_models.Push_Up_Counter import process_frame as pushUpCount
from CV_models.squats import process_frame as squatsExercise

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


@app.websocket("/cv/dumbell")
async def dumbell(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            processed_img_str, count = dumbbellExercise(frame_data)
            response = {
                "image": f"data:image/jpeg;base64,{processed_img_str}",
                "count": count,
            }
            await websocket.send_json(response)
    except WebSocketDisconnect as e:
        print(f"Connection error: {e}")


@app.websocket("/cv/shldpress")
async def shldpress(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            processed_img_str, count = shldpressExercise(frame_data)
            response = {
                "image": f"data:image/jpeg;base64,{processed_img_str}",
                "count": count,
            }
            await websocket.send_json(response)
    except WebSocketDisconnect as e:
        print(f"Connection error: {e}")


@app.websocket("/cv/pushup")
async def pushUp(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            processed_img_str, count = pushUpCount(frame_data)
            response = {
                "image": f"data:image/jpeg;base64,{processed_img_str}",
                "count": count,
            }
            await websocket.send_json(response)
    except WebSocketDisconnect as e:
        print(f"Connection error: {e}")


@app.websocket("/cv/squats")
async def squats(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            processed_img_str, count = squatsExercise(frame_data)
            response = {
                "image": f"data:image/jpeg;base64,{processed_img_str}",
                "count": count,
            }
            await websocket.send_json(response)
    except WebSocketDisconnect as e:
        print(f"Connection error: {e}")
