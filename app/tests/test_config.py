import os
from dotenv import load_dotenv
load_dotenv()
class TestConfig:
    SQL_ALCHEMY_ECHO = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use file-based database
    SECRET_KEY = os.getenv('TEST_SECRET_KEY')
    WTF_CSRF_ENABLED = False
