import os
import requests

REFRESH_URL = (
    "https://adbackend.annadarpan.in/"
    "prdannadarpan.in/usermanagement/api/v3/auth/refresh-token"
)

token = os.environ["ANNA_REFRESH_TOKEN"]
client_id = os.getenv("ANNA_CLIENT_ID", "ad-fci")

r = requests.post(
    REFRESH_URL,
    params={
        "refreshToken": token,
        "clientId": client_id,
    },
    headers={
        "Accept": "application/json",
        "Origin": "https://www.annadarpan.in",
        "Referer": "https://www.annadarpan.in/",
    },
    timeout=30,
)

print("Refresh HTTP status:", r.status_code)
r.raise_for_status()

data = r.json()

if not data.get("access_token"):
    raise RuntimeError("No access token returned")

if not data.get("refresh_token"):
    raise RuntimeError("No new refresh token returned")

# Save only for this workflow/job.
# Do NOT print either token.
with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"ANNA_ACCESS_TOKEN={data['access_token']}\n")
    f.write(f"ANNA_REFRESH_TOKEN_NEW={data['refresh_token']}\n")

print("Access token: PRESENT")
print("New refresh token: PRESENT")
print("expires_in:", data.get("expires_in"))
print("refresh_expires_in:", data.get("refresh_expires_in"))
