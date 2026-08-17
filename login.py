import os
import sys
import base64
import json
import requests

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


LOGIN_URL = os.getenv(
    "LOGIN_URL",
    "https://adbackend.annadarpan.in/prdannadarpan.in/security/passwordLogin"
)

REFRESH_URL = os.getenv(
    "REFRESH_URL",
    "https://adbackend.annadarpan.in/prdannadarpan.in/api/v3/auth/refresh-token"
)

CLIENT_ID = os.getenv("CLIENT_ID", "ad-fci")

user = os.environ["ANNADARPAN_USERNAME"]
password = os.environ["ANNADARPAN_PASSWORD"]
key_b64 = os.environ["ANNADARPAN_PUBLIC_KEY_B64"]

# CAPTCHA token फक्त उपलब्ध असेल तर वापरला जाईल
captcha = os.getenv("ANNADARPAN_CAPTCHA_TOKEN", "")


# ============================================================
# 1. PASSWORD ENCRYPTION
# ============================================================

pem = (
    "-----BEGIN PUBLIC KEY-----\n"
    + key_b64.strip()
    + "\n-----END PUBLIC KEY-----\n"
).encode()

key = serialization.load_pem_public_key(pem)

encrypted = key.encrypt(
    password.encode(),
    padding.PKCS1v15()
)


# ============================================================
# 2. LOGIN PAYLOAD
# ============================================================

payload = {
    "username": user,
    "clientId": CLIENT_ID,
    "password": base64.b64encode(encrypted).decode()
}

if captcha:
    payload["tokenCaptcha"] = captcha


# ============================================================
# 3. LOGIN
# ============================================================

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://www.annadarpan.in",
    "Referer": "https://www.annadarpan.in/"
}

print("=" * 60)
print("ANNA DARPAN LOGIN")
print("=" * 60)

r = requests.post(
    LOGIN_URL,
    json=payload,
    headers=headers,
    timeout=30
)

print("Login HTTP status:", r.status_code)

if not r.ok:
    print("Login failed:")
    print(r.text)
    sys.exit(1)

try:
    login_data = r.json()
except ValueError:
    print("Login response JSON नाही")
    print(r.text)
    sys.exit(1)


# ============================================================
# 4. TOKEN CHECK
# ============================================================

access_token = login_data.get("access_token")
refresh_token = login_data.get("refresh_token")

if not access_token:
    print("access_token मिळाला नाही.")
    print(json.dumps(login_data, indent=2))
    sys.exit(1)

print("✓ Login successful")
print("✓ Access token received")

if refresh_token:
    print("✓ Refresh token received")
else:
    print("⚠ Refresh token मिळाला नाही")


# ============================================================
# 5. REFRESH TOKEN TEST
# ============================================================

if refresh_token:

    print()
    print("=" * 60)
    print("TESTING OFFICIAL REFRESH TOKEN")
    print("=" * 60)

    refresh_response = requests.post(
        REFRESH_URL,
        params={
            "refreshToken": refresh_token,
            "clientId": CLIENT_ID
        },
        headers={
            "Accept": "application/json"
        },
        timeout=30
    )

    print("Refresh HTTP status:", refresh_response.status_code)

    if refresh_response.ok:

        try:
            refresh_data = refresh_response.json()
        except ValueError:
            print("Refresh response JSON नाही")
            print(refresh_response.text)
            sys.exit(1)

        new_access_token = refresh_data.get("access_token")
        new_refresh_token = refresh_data.get(
            "refresh_token",
            refresh_token
        )

        if new_access_token:
            access_token = new_access_token
            refresh_token = new_refresh_token

            print("✓ Access token successfully refreshed")
            print("✓ New token ready for API calls")

        else:
            print("⚠ Refresh response मध्ये access_token नाही")
            print(json.dumps(refresh_data, indent=2))
            sys.exit(1)

    else:
        print("Refresh failed:")
        print(refresh_response.text)
        sys.exit(1)


# ============================================================
# 6. SAVE TOKENS FOR NEXT STEPS
# ============================================================

with open("anna_tokens.json", "w") as f:
    json.dump(
        {
            "access_token": access_token,
            "refresh_token": refresh_token
        },
        f
    )

print()
print("=" * 60)
print("SUCCESS")
print("=" * 60)
print("✓ Login")
print("✓ Access token")
print("✓ Refresh token")
print("✓ Refresh API")
print("✓ Token ready for DSI / DSR API calls")
