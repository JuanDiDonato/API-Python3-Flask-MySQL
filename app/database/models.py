# Paquetes
from .db import db

# Modelos
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(70), unique=True)
    password = db.Column(db.VARCHAR(70))

    def __init__(self,username,password):
        self.username = username
        self.password = password

class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    title = db.Column(db.String(70))
    description = db.Column(db.String(100))

    def __init__(self, title, description,id):
        self.title = title
        self.description = description
        self.id = id



