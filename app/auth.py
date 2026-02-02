from fastapi import Header, HTTPException
from typing import Optional

API_KEY = "CHANGE_THIS_SECRET_KEY"

def verify_api_key(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split(" ")[1]

    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
