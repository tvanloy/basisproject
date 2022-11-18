import fastapi
from fastapi import FastAPI
import service
import fastapi.responses as responses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "The meme api"}


@app.get("/wholesome-memes")
def get_wholesomememes():
    img_path = service.random_img("wholesomememes")
    return responses.FileResponse(img_path)

@app.post("/post-wholesome-memes")
def create_programmer(image: fastapi.UploadFile = fastapi.File(...)):
    file_path = service.upload_image("programmerhumor", image)
    if file_path is None:
        return fastapi.HTTPException(status_code=409)
    return responses.FileResponse(file_path)


@app.get("/programmerhumor")
def get_wholesomememes():
    img_path = service.random_img("programmerhumor")
    return responses.FileResponse(img_path)


@app.post("/post-programmer-memes")
def create_programmer(image: fastapi.UploadFile = fastapi.File(...)):
    file_path = service.upload_image("programmerhumor", image)
    if file_path is None:
        return fastapi.HTTPException(status_code=409)
    return responses.FileResponse(file_path)
