import fastapi
from fastapi import FastAPI
import fastapi.responses as responses
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import random
import time

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


def get_image_files(directory_name: str) -> List[str]:
    return os.listdir("prank")


def random_img(directory_name: str) -> str:
    images = get_image_files(directory_name)
    random_image = random.choice(images)
    path = f"{directory_name}/{random_image}"
    return path


def is_image(filename: str) -> bool:
    valid = (".png", ".jpg", ".jpeg", ".gif")
    return filename.endswith(valid)


def upload_image(directory_name: str, image: fastapi.UploadFile):
    if is_image(image.filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        image_name = timestr + image.filename.replace(' ', '-')
        with open(f"{directory_name}/{image_name}", "wb") as image_upload:
            image_upload.write(image.file.read())
        return f"{directory_name}/{image_name}"
    return None


@app.get("/")
def root():
    return {"message": "The meme api"}


@app.get("/wholesome-memes")
def get_wholesomememes():
    img_path = random_img("wholesomememes")
    return responses.FileResponse(img_path)


@app.post("/post-wholesome-memes")
def create_programmer(image: fastapi.UploadFile = fastapi.File(...)):
    file_path = upload_image("programmerhumor", image)
    if file_path is None:
        return fastapi.HTTPException(status_code=409)
    return responses.FileResponse(file_path)


@app.get("/programmerhumor")
def get_wholesomememes():
    img_path = random_img("programmerhumor")
    return responses.FileResponse(img_path)


@app.post("/post-programmer-memes")
def create_programmer(image: fastapi.UploadFile = fastapi.File(...)):
    file_path = upload_image("programmerhumor", image)
    if file_path is None:
        return fastapi.HTTPException(status_code=409)
    return responses.FileResponse(file_path)
