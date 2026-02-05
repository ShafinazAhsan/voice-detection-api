import os
from fastapi import HTTPException
from dotenv import load_dotenv

# We only load .env if we are not in a production environment like Railway
# (Railway provides these directly in the environment)
if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()

def verify_api_key(provided_key: str):
    """
    Robust API Key validation that handles Railway environment variables
    and potential whitespace issues.
    """
    # 1. Fetch from environment (this is what Railway uses)
    expected_key = os.getenv("API_KEY")

    # 2. Safety check: If not found, try reloading env (fallback)
    if not expected_key:
        load_dotenv()
        expected_key = os.getenv("API_KEY")

    # 3. Handle missing configuration on server
    if not expected_key:
        print("CRITICAL: API_KEY environment variable is not set!")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: API_KEY not found."
        )

    # 4. Handle missing header in request
    if not provided_key:
        raise HTTPException(
            status_code=401,
            detail="API key header (X-API-KEY) is missing."
        )

    # 5. Clean and compare (strip whitespace to prevent paste errors)
    provided_clean = provided_key.strip()
    expected_clean = expected_key.strip()

    if provided_clean != expected_clean:
        print(f"AUTH FAILED: Provided key dose not match expected key.")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )
    
    return True
