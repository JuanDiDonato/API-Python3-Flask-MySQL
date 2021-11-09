# Modulos
from flask import Flask

# Paquetes
from controllers import users
from ext import jwt
from ext import ma, jwt
from database.db import db
from config import default

app = Flask(__name__)

app.config.from_object(default)
ma.init_app(app)
db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

#Routes
#POST REQUEST
@app.route('/register', methods=['POST'])
def register():
    return(users.addUser(db))

@app.route('/login', methods=['POST'])
def login():
    return(users.loginUser(db))

@app.route('/create', methods=['POST'])
def create():
    return(users.create(db))

@app.route('/logout', methods=['POST'])
def logout():
    return(users.clearCookie())

#GET REQUEST
@app.route('/tasks', methods=['GET'])
def tasks():
    return(users.get_tasks(db))

@app.route('/tasks/<id>', methods=['GET'])
def task(id):
    return(users.get_id_tasks(id,db))

#PUT REQUEST
@app.route('/tasks/<id>', methods=['PUT'])
def edit(id):
    return(users.edit_id_task(id, db))

#DELETE REQUEST
@app.route('/tasks/<id>', methods=['DELETE'])
def delete(id):
    return(users.delete_id_task(id, db))
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)