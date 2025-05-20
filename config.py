import os
from dotenv import load_dotenv
import datetime
load_dotenv()
class Config:
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv("SECRET_KEY")
  JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours = 2)