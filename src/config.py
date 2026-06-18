import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "DriveChatbot"
APP_VERSION = "0.1.0"

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")