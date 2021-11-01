from flask_jwt_extended import JWTManager
#Variables de entorno
import os
from dotenv import load_dotenv

#Obtengo las variables de entorno desde mi archivo .env
load_dotenv()
KEY = os.getenv('KEY')


def configureJWT(app):
     app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
     app.config["JWT_COOKIE_SECURE"] = False
     app.config["JWT_SECRET_KEY"] = KEY
     jwt = JWTManager(app)
     return jwt

