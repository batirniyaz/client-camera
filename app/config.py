import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

BASE_URL = os.getenv("BASE_URL")

SECRET_AUTH = os.getenv("SECRET_AUTH")

if not all([DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT]):
    raise ValueError("One or more environment variables are missing")

if not BASE_URL:
    raise ValueError("BASE_URL is not set in the environment variables")

if not SECRET_AUTH:
    raise ValueError("SECRET_AUTH is not set in the environment variables")
