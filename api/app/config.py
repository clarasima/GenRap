import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_URI = os.environ.get('DB_URI')
    SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY')

config = Config()


