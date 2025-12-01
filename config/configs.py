import os
from dotenv import load_dotenv

load_dotenv()


API_BASE_URL = os.getenv("BASE_URL")
OAUTH_TOKEN = os.getenv("TOKEN")

