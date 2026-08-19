import os
import sys
import requests


REFRESH_URL = (
    "https://adbackend.annadarpan.in/"
    "prdannadarpan.in/usermanagement/api/v3/auth/refresh-token"
)

# GitHub Actions Secret
refresh_token = os.environ.get("ANNA_REFRESH_TOKEN")

if not refresh_token:
    print("ERROR: ANNA_REFRESH_TOKEN secret is not set.")
    sys.exit(1)

client_id = os.getenv("ANNA_CLIENT_ID", "ad-fci")


try:
    response = requests.post(
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

except requests.RequestException as e:
    print("ERROR: Refresh request failed.")
    print(type(e).__name__)
    sys.exit(1)


print("Refresh HTTP status:", response.status_code)

if not response.ok:
    print("Refresh failed.")

    # Response मध्ये token असण्याची शक्यता असल्यामुळे
    # response body पूर्ण print करत नाही.
    try:
        data = response.json()

        if isinstance(data, dict):
            print("Error:", data.get("error", "Unknown error"))
            print("Message:", data.get("message", ""))
        else:
            print("Non-object error response.")

    except ValueError:
        print("Non-JSON error response.")

    sys.exit(1)


try:
    data = response.json()

except ValueError:
    print("ERROR: Refresh response was not JSON.")
    sys.exit(1)


# ---------------------------------------------------------
# Validate returned tokens
# ---------------------------------------------------------

access_token = data.get("access_token")
new_refresh_token = data.get("refresh_token")

if not access_token:
    print("ERROR: No access token returned.")
    sys.exit(1)

if not new_refresh_token:
    print("ERROR: No new refresh token returned.")
    sys.exit(1)


# ---------------------------------------------------------
# Save tokens only for the current GitHub Actions job
#
# These values will NOT be printed.
# The next workflow step can read them.
# ---------------------------------------------------------

github_env = os.environ.get("GITHUB_ENV")

if not github_env:
    print("ERROR: GITHUB_ENV is not available.")
    sys.exit(1)


with open(github_env, "a", encoding="utf-8") as f:
    f.write(f"ANNA_ACCESS_TOKEN={access_token}\n")
    f.write(f"ANNA_REFRESH_TOKEN_NEW={new_refresh_token}\n")


# ---------------------------------------------------------
# Safe output
# ---------------------------------------------------------

print("Access token: PRESENT")
print("New refresh token: PRESENT")
print("expires_in:", data.get("expires_in"))
print("refresh_expires_in:", data.get("refresh_expires_in"))
print("token_type:", data.get("token_type", ""))
print("scope:", data.get("scope", ""))

print("Refresh completed successfully.")
