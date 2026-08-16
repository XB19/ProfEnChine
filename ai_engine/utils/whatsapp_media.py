import requests

def get_media_url(media_id, token):
    url = f"https://graph.facebook.com/v22.0/{media_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers)

    data = r.json()

    if "url" not in data:
        raise Exception(f"Erreur Meta: {data}")

    return data["url"]



import os
import requests

def download_pdf(media_url, token, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(media_url, headers=headers)

    if r.status_code != 200:
        raise Exception(f"Download error: {r.text}")

    with open(save_path, "wb") as f:
        f.write(r.content)

    return save_path