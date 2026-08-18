import os
import requests

REFRESH_URL = "https://adbackend.annadarpan.in/prdannadarpan.in/usermanagement/api/v3/auth/refresh-token"

refresh_token = os.environ["ANNA_REFRESH_TOKEN"]
client_id = os.getenv("ANNA_CLIENT_ID", "ad-fci")

r = requests.post(
    REFRESH_URL,
    params={
        "refreshToken": refresh_token,
        "clientId": client_id,
    },
    headers={
        "Accept": "application/json",
        "Origin": "https://www.annadarpan.in",
        "Referer": "https://www.annadarpan.in/",
    },
    timeout=30,
)

print("HTTP status:", r.status_code)

try:
    data = r.json()

    if isinstance(data, dict):
        print("Fields returned:", list(data.keys()))

        for key in ("access_token", "refresh_token"):
            if key in data:
                value = data[key]
                print(
                    f"{key}: PRESENT "
                    f"(length={len(value) if isinstance(value, str) else 'unknown'})"
                )

        for key in ("expires_in", "refresh_expires_in", "token_type", "scope"):
            if key in data:
                print(f"{key}: {data[key]}")

    else:
        print("Response:", data)

except ValueError:
    print("Non-JSON response:", r.text[:500])

r.raise_for_status()
