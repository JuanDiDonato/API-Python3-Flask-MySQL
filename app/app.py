from flask import Flask
from database import connection
from controllers import users
from config import Jwt

app = Flask(__name__)
mysql = connection.configureMySQL(app)
jwt = Jwt.configureJWT(app)

#Routes
#POST REQUEST
@app.route('/register', methods=['POST'])
def register():
    return(users.addUser(mysql))

@app.route('/login', methods=['POST'])
def login():
    return(users.loginUser(mysql))

@app.route('/create', methods=['POST'])
def create():
    return(users.create(mysql))

#GET REQUEST
@app.route('/tasks', methods=['GET'])
def tasks():
    return(users.get_tasks(mysql))

@app.route('/tasks/<id>', methods=['GET'])
def task(id):
    return(users.get_id_tasks(id,mysql))

#PUT REQUEST
@app.route('/tasks/<id>', methods=['PUT'])
def edit(id):
    return(users.edit_id_task(id, mysql))

#DELETE REQUEST
@app.route('/tasks/<id>', methods=['DELETE'])
def delete(id):
    return(users.delete_id_task(id, mysql))
    


if __name__ == '__main__':
    app.run(debug=True)