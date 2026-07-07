import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "DriveChatbot"
APP_VERSION = "0.1.0"

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
GOOGLE_SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_SERVICE_ACCOUNT_INFO")

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_PATH = os.getenv("QDRANT_PATH", "data/qdrant")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "drive_documents")

SYNC_DATABASE_PATH = os.getenv("SYNC_DATABASE_PATH", "data/sync.db")