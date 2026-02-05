import sys
import os

# Add current directory and 'app' directory to sys.path
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app'))

try:
    from app.main import app
    print("Successfully imported FastAPI app from app.main")
except ImportError as e:
    print(f"Failed to import app: {e}")
    # Fallback if Vercel restructure movements occur
    try:
        from main import app
        print("Successfully imported FastAPI app from root main")
    except ImportError:
        raise e
