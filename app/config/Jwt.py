from flask_jwt_extended import JWTManager
import os

def configureJWT(app):
     app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
     app.config["JWT_COOKIE_SECURE"] = False
     app.config["JWT_SECRET_KEY"] = 'm1ch0'
     jwt = JWTManager(app)
     return jwt

