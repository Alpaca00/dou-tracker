import os

from dotenv import load_dotenv

load_dotenv()

class Environment:
    """A class for managing environment variables."""
    API_KEY = os.environ.get("API_KEY")