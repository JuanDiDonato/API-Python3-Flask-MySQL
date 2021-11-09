# Modulos
import os

from dotenv import load_dotenv

load_dotenv() # Obtengo las variables de entorno desde mi archivo .env
KEY = os.getenv('KEY')
FLASK_KEY = os.getenv('FLASK_KEY')
DATABASE = os.getenv('DATABASE')

# Flask
SECRET_KEY = FLASK_KEY

# MySQL
SQLALCHEMY_DATABASE_URI = DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_TOKEN_LOCATION = ["headers", "cookies"]
JWT_COOKIE_SECURE = False
JWT_SECRET_KEY = KEY


