import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.DB_NAME = os.getenv('DB_NAME', 'database.sqlite3')
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'secret')


config = Config()
