from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dumbell_curl import process_frame

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/dumbell")
async def dumbell(file: UploadFile = File(...)):
    contents = await file.read()
    img_str = process_frame(contents)
    return JSONResponse(content={"image": f"data:image/jpeg;base64,{img_str}"})
