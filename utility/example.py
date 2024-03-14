"""Google Login Example
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi_sso.sso.facebook import FacebookSSO

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_ID = "603857304441893"
CLIENT_SECRET = "a041ae17da226a21dd94311f177f2abd"

app = FastAPI()

sso = FacebookSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:5000/auth/callback",
    allow_insecure_http=True,
    use_state=False,
)


@app.get("/auth/login")
async def auth_init():
    """Initialize auth and redirect"""
    return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Verify login"""
    user = await sso.verify_and_process(request)
    print(user)
    return "here is the authentication token"


if __name__ == "__main__":
    try:
        uvicorn.run(app="example:app", host="127.0.0.1", port=5000)
    except KeyboardInterrupt:
        pass
