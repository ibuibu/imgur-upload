import io
import os
import json
from dotenv import load_dotenv
from PIL import ImageGrab
import requests

load_dotenv()

refresh_token = os.getenv("REFRESH_TOKEN")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def main():
    access_token = generate_access_token(refresh_token, client_id, client_secret)
    image_binary = get_clipboard_image_binary()
    link = upload(access_token, image_binary)
    print(link)


def generate_access_token(refresh_token, client_id, client_secret):
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }
    r = requests.post("https://api.imgur.com/oauth2/token", data=data)
    return json.loads(r.text)["access_token"]


def get_clipboard_image_binary():
    clipboard_image = ImageGrab.grabclipboard()
    img_bytes = io.BytesIO()
    clipboard_image.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


def upload(access_token, image_binary):
    # 匿名モード
    # headers = {
    #     "authorization": f"Client-ID {client_id}",
    # }

    headers = {
        "authorization": f"Bearer {access_token}",
    }

    files = {
        "image": image_binary,
    }

    r = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)
    return json.loads(r.text)["data"]["link"]


if __name__ == "__main__":
    main()
