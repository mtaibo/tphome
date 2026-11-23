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
    # Browsers carry the session in a cookie, the apps as a bearer token: pass on whichever came.
    headers = {k: v for k in ("cookie", "authorization") if (v := request.headers.get(k))}
    if not headers:
        raise HTTPException(status_code=401, detail="Not authenticated")

    req = urllib.request.Request(f"{AUTH_URL}/auth/passkey/me", headers=headers)
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
