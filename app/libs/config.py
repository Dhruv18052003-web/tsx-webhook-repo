"""
Central configuration object for the Flask app.

Located at: dev.env
"""

from pathlib import Path
import os
import sys
from urllib.parse import quote_plus

# Lib to load the env variables from dev.env  
from dotenv import load_dotenv



# ---------------------------------------------------------------------------
# Locate and read the .env file (we go two levels up: /app → project root)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]      # points to project root file

# This represents development enviorment 
env_name = "dev"

env_file = BASE_DIR / f"{env_name}.env"

if not env_file.exists():
    raise FileNotFoundError(f"Environment file '{env_file}' not found.")

load_dotenv(dotenv_path=env_file)

class Config:
    # Running Environment
    RUN_ENV = env_name

    # MongoDB configuration
    DB_PROTOCOL=os.getenv("DB_PROTOCOL")
    DB_HOST=os.getenv("DB_HOST")
    DB_PORT=os.getenv("DB_PORT")
    DB_USERNAME=quote_plus(os.getenv("DB_USERNAME") or "")
    DB_PASSWORD=quote_plus(os.getenv("DB_PASSWORD") or "")

    DB_CON_STR = f"{DB_PROTOCOL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    DB_NAME = os.getenv("DB_NAME")
    
    # Storage
    BASE_DIR = BASE_DIR
    STORAGE_PATH = BASE_DIR / os.getenv("STORAGE_PATH")
    LOG_PATH = STORAGE_PATH / os.getenv("LOG_PATH")
    APP_LOG_PATH = LOG_PATH / os.getenv("APP_LOG_PATH")
    SYS_LOG_PATH = LOG_PATH / os.getenv("SYS_LOG_PATH")

# cONFIG IS THE FILE where variables from env file has been loaded into the development condiguration.
# We can make env file for different enviorment like developmwnt and testing. And then use them in config .
