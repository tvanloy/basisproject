from typing import List
import os
import random
import fastapi
import time


def get_image_files(directory_name: str) -> List[str]:
    return os.listdir(directory_name)


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