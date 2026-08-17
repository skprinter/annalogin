import os, sys, base64, json, requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

URL = os.getenv("LOGIN_URL", "https://adbackend.annadarpan.in/prdannadarpan.in/security/passwordLogin")
user = os.environ["ANNADARPAN_USERNAME"]
password = os.environ["ANNADARPAN_PASSWORD"]
key_b64 = os.environ["ANNADARPAN_PUBLIC_KEY_B64"]
captcha = os.getenv("ANNADARPAN_CAPTCHA_TOKEN", "")

pem = ("-----BEGIN PUBLIC KEY-----\n" + key_b64.strip() +
       "\n-----END PUBLIC KEY-----\n").encode()
key = serialization.load_pem_public_key(pem)
encrypted = key.encrypt(password.encode(), padding.PKCS1v15())
payload = {"username": user, "clientId": os.getenv("CLIENT_ID", "ad-fci"),
           "password": base64.b64encode(encrypted).decode()}
if captcha:
    payload["tokenCaptcha"] = captcha

r = requests.post(URL, json=payload, headers={
    "Accept":"application/json", "Content-Type":"application/json",
    "Origin":"https://www.annadarpan.in", "Referer":"https://www.annadarpan.in/"
}, timeout=30)
print("HTTP status:", r.status_code)
try:
    x = r.json()
    if isinstance(x, dict):
        x = {k: ("***REDACTED***" if any(s in k.lower() for s in
             ("token","authorization","access","refresh","secret")) else v)
             for k,v in x.items()}
    print("Response:", json.dumps(x, ensure_ascii=False))
except ValueError:
    print("Non-JSON response")
sys.exit(0 if r.ok else 1)
