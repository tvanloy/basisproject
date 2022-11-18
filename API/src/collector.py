import os
import dotenv
import praw
import urllib.parse as parse
import requests
import shutil

dotenv.load_dotenv()


def create_reddit_client():
    client = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        user_agent=os.environ["USER_AGENT"],
    )
    return client


def is_image(post):
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False


def get_img(client: praw.Reddit, subreddit_name: str, limit: int):
    hotMemes = client.subreddit(subreddit_name).hot(limit=limit)
    img_urls = list()
    for post in hotMemes:
        if is_image(post):
            img_urls.append(post.url)
    return img_urls


def get_img_name(image_url: str) -> str:
    img_name = parse.urlparse(image_url)
    return os.path.basename(img_name.path)


def create_folder(folder_name: str):
    try:
        os.mkdir(folder_name)
    except OSError:
        print("something happened")
        # absolute_path = _os.path.abspath("wholesomememes")
        # print("Full path: " + absolute_path)
        # print("Directory Path: " + _os.path.dirname(absolute_path))
    else:
        print("folder created")


def download_image(folder_name: str, raw_response, image_name: str):
    create_folder(folder_name)
    with open(f"{folder_name}/{image_name}", "wb") as img_file:
        shutil.copyfileobj(raw_response, img_file)


def collect(subreddit_name: str, limit: int = 20):
    client = create_reddit_client()
    img_urls = get_img(
        client=client, subreddit_name=subreddit_name, limit=limit
    )
    for img in img_urls:
        img_name = get_img_name(img)
        response = requests.get(
            img, stream=True
        )
        if response.status_code == 200:
            response.raw.decode_content = True
            download_image(
                subreddit_name, response.raw, img_name
            )


if __name__ == "__main__":
    collect("programmerhumor")
