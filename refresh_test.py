import os
import requests

REFRESH_URL = (
    "https://adbackend.annadarpan.in/"
    "prdannadarpan.in/usermanagement/api/v3/auth/refresh-token"
)

CLIENT_ID = os.getenv("ANNA_CLIENT_ID", "ad-fci")


def refresh(token):
    r = requests.post(
        REFRESH_URL,
        params={
            "refreshToken": token,
            "clientId": CLIENT_ID,
        },
        headers={
            "Accept": "application/json",
            "Origin": "https://www.annadarpan.in",
            "Referer": "https://www.annadarpan.in/",
        },
        timeout=30,
    )

    print("HTTP status:", r.status_code)

    if not r.ok:
        print("Refresh failed:", r.text[:500])
        return None

    data = r.json()

    print("Fields:", list(data.keys()))
    print("Access token:", "PRESENT" if data.get("access_token") else "MISSING")
    print("Refresh token:", "PRESENT" if data.get("refresh_token") else "MISSING")
    print("expires_in:", data.get("expires_in"))
    print("refresh_expires_in:", data.get("refresh_expires_in"))

    return data


# Token A
token_a = os.environ["ANNA_REFRESH_TOKEN"]

print("========== REFRESH #1 ==========")
result_1 = refresh(token_a)

if not result_1 or not result_1.get("refresh_token"):
    raise SystemExit("No new refresh token returned.")

# Token B
token_b = result_1["refresh_token"]

print("\n========== REFRESH #2 ==========")
result_2 = refresh(token_b)

if not result_2:
    raise SystemExit("Second refresh failed.")

print("\n========== RESULT ==========")
print("Token A -> Token B: SUCCESS")
print(
    "Token B -> Token C:",
    "SUCCESS" if result_2.get("refresh_token") else "NO NEW TOKEN"
)
