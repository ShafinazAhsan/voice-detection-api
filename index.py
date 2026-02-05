import sys
import os

# Ensure the 'app' directory is in the python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app

# This shim allows Vercel to see the requirements.txt in the root
# while keeping your logic inside the /app directory.
