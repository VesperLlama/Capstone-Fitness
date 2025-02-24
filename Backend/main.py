from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
from dotenv import load_dotenv
from pymongo import MongoClient
from CV_models.dumbell_curl import process_frame as dumbbell
from CV_models.Shoulderpress import process_frame as shldpress

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register():
    return True


@app.post("/login")
async def login():
    return True


@app.post("/addData")
async def addData():
    pass


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
