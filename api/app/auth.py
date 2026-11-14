from fastapi import HTTPException, Request
import urllib.request
import urllib.error
import json
import os

# tpcloud's auth service, reached through the tpcloud_gateway network the API shares with it
AUTH_URL = os.getenv("AUTH_URL", "http://auth:8000")


def require_admin(request: Request) -> dict:
    """The gateway only checks that someone is signed in, so admin-only routes ask tpcloud
    auth who owns the session on every call (no cache, a demoted admin loses access at once)."""
    cookie = request.headers.get("cookie", "")
    if not cookie:
        raise HTTPException(status_code=401, detail="Not authenticated")

    req = urllib.request.Request(f"{AUTH_URL}/auth/passkey/me", headers={"cookie": cookie})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            user = json.loads(resp.read())
    except urllib.error.HTTPError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise HTTPException(status_code=503, detail="Auth service unavailable")

    if user.get("is_admin") is not True:
        raise HTTPException(status_code=403, detail="Admin only")
    return user
