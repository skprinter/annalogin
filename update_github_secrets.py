import os
import base64
import json
import requests
from nacl import encoding, public

OWNER = os.environ["GITHUB_REPOSITORY"].split("/")[0]
REPO = os.environ["GITHUB_REPOSITORY"].split("/")[1]
GH_TOKEN = os.environ["GH_SECRETS_TOKEN"]

ACCESS_TOKEN = os.environ["ANNA_ACCESS_TOKEN"]
REFRESH_TOKEN = os.environ["ANNA_REFRESH_TOKEN_NEW"]

headers = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Get repository public key
url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/public-key"

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()
key_data = r.json()

public_key = public.PublicKey(
    key_data["key"].encode(),
    encoding.Base64Encoder
)

def encrypt_secret(value):
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(value.encode())
    return base64.b64encode(encrypted).decode()

def update_secret(name, value):
    url = (
        f"https://api.github.com/repos/{OWNER}/{REPO}"
        f"/actions/secrets/{name}"
    )

    payload = {
        "encrypted_value": encrypt_secret(value),
        "key_id": key_data["key_id"],
    }

    r = requests.put(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    r.raise_for_status()
    print(f"{name}: UPDATED")

update_secret("ANNA_ACCESS_TOKEN", ACCESS_TOKEN)
update_secret("ANNA_REFRESH_TOKEN", REFRESH_TOKEN)

print("GitHub Anna Darpan tokens updated successfully.")
