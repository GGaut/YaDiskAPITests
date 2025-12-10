import os

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
RESOURCE_ENDPOINT = os.getenv("RESOURCE_ENDPOINT")
TRASH_ENDPOINT = os.getenv("TRASH_ENDPOINT")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
