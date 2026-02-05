import os
from fastapi import HTTPException
from dotenv import load_dotenv

# Load variables from environment
load_dotenv()

def verify_api_key(provided_key: str):
    # Get the key from the server's environment variables
    # This is what you set in the Railway 'Variables' tab
    expected_key = os.getenv("API_KEY")

    if not provided_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )

    if provided_key != expected_key:
        # Debugging aid: In production, you might not want to show what the expected key is
        # but while we fix this, let's make sure it's not simply empty
        if not expected_key:
            raise HTTPException(
                status_code=500,
                detail="Server configuration error: API_KEY not set on server"
            )
            
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return True
