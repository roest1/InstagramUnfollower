import os

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
TWO_FACTOR = os.getenv("TWO_FACTOR")
USERNAMES_FILENAME = os.getenv("USERNAMES_FILENAME")
