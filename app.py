#Python3 Modules
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import bcrypt

app = Flask(__name__)

#JWT config
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = "m1ch0"
#MySQL config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tareas'

mysql = MySQL(app)
jwt = JWTManager(app)

#Routes

#New Users
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    if username == '' or password == '':
        return jsonify({'message':{'msj':'Por favor complete todos los campos', 'msjE':True}})
    else:
        cur = mysql.connection.cursor()
        user = cur.execute('SELECT * FROM users WHERE username = %s',(username,))
        if user:
            return jsonify({'message':{'msj':'Este nombre de usuario ya esta registrado', 'msjE':True}})
        else: 
            password = password.encode()  # codifico la cadena  
            sal = bcrypt.gensalt()  # cantidad de encriptaciones (12)
                # encripta la contraseña a encriptar las 12 veces
            password_s = bcrypt.hashpw(password, sal)
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password_s))
            mysql.connection.commit()
            return jsonify({'message':{'msj':"Registrado exitosamente", 'msjE' : False}})
                
    
    

#Login

@app.route('/login', methods=['POST'])
def login():
    request.method == 'POST'
    user = request.json['username']
    password = request.json['password']
    password = password.encode()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s',(user,))
    data = cur.fetchall()
    if data:
        datas = data[0]
        password_f = datas[2]
        id = datas[0]
        user = (datas[0], datas[1])
        password_f = password_f.encode()
        if bcrypt.checkpw(password, password_f):
            access_token = create_access_token(identity=[user,id])
            res = jsonify({'isAuth':True, 'user' : user})

            return jsonify({'token': access_token, 'isAuth' : True})
        else:
            return jsonify({'message':{'msj':"¡Contraseña incorrecta!", 'isAuth' : False}})
    else:
        return jsonify({'message':{'msj':"¡Usuario no encontrado!", 'isAuth' : False}})


#New task
@app.route('/create', methods=['POST'])
@jwt_required()
def create():
    info = get_jwt_identity()
    id_user = info[1]
    title = request.json['title']
    description = request.json['description']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO tasks (id_user, title, description) VALUES (%s, %s, %s)', (id_user, title, description))
    mysql.connection.commit()
    return jsonify({"EXITO" : "Nota creada con exito" })

#All taks
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    info = get_jwt_identity()
    id_user = str(info[1])
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tasks WHERE id_user = %s', (id_user))
    tasks = cur.fetchall()
    mysql.connection.commit()
    return jsonify(tasks)

#Id task
@app.route('/tasks/<id>', methods=['GET'])
@jwt_required()
def get_id_tasks(id):
    info = get_jwt_identity()
    id_user = str(info[1])
    cur = mysql.connection.cursor()
    tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
    if tasks_user:
        task = cur.fetchall()
        mysql.connection.commit()
        return jsonify(task)
    else:
        return jsonify({"ERR0R":"ACCESO DENEGAD0"})


#Edit task
@app.route('/tasks/<id>', methods=['PUT'])
@jwt_required()
def edit_id_task(id):
    info = get_jwt_identity()
    id_user = str(info[1])
    cur = mysql.connection.cursor()
    tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
    if tasks_user:
        title= request.json['title']
        description= request.json['description']
        cur.execute('UPDATE tasks SET title = %s, description = %s  WHERE tasks.id_task = %s',(title, description, id))
        mysql.connection.commit()
        return jsonify({'EXITO':'Datos actualizados correctamente'})
    else:
        mysql.connection.commit()
        return jsonify({"ERR0R":"ACCESO DENEGAD0"})
    
    

#Delete task
@app.route('/tasks/<id>', methods=['DELETE'])
@jwt_required()
def delete_id_task(id):
    info = get_jwt_identity()
    id_user = str(info[1])
    cur = mysql.connection.cursor()
    tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
    if tasks_user:
        cur.execute('DELETE FROM tasks WHERE tasks.id_task = %s', (id))
        mysql.connection.commit()
        return jsonify({'EXITO':'Datos eliminados correctamente'})
    else:
        mysql.connection.commit()
        return jsonify({"ERR0R":"ACCESO DENEGAD0"})

    

if __name__ == '__main__':
    app.run(debug=True)
