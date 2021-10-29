from config import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

#Registrar usuario
def addUser(mysql):
     username = request.json['username']
     password = request.json['password']
     if password and username :
          cur = mysql.connection.cursor()
          user = cur.execute('SELECT * FROM users WHERE username = %s', [username])
          if user !=0:
               mysql.connection.commit()
               return jsonify(message="Nombre de usuario en uso.", error = True),422
          else: 
               encryptedPassword = bcrypt.hashPassword(password)
               cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, encryptedPassword))
               mysql.connection.commit()
               return jsonify(message ="Registrado exitosamente", error = False), 201
     else: return jsonify(message="Complete todos los campos", error = True), 400

#Loguear usuario
def loginUser(mysql):
     username = request.json['username']
     password = request.json['password']
     if password and username :
          password = password.encode()
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM users WHERE username = %s', [username])
          userData = cur.fetchall()
          if userData:
               password_f = userData[0][2]
               id = userData[0][0]
               username = userData[0][1]
               user = (id,username)
               dbPassword= password_f.encode()
               checkPassword = bcrypt.comparePassword(password, dbPassword)
               if checkPassword:
                    access_token = create_access_token(identity=[user,id])
                    return jsonify(token = access_token, isAuth = True), 200
               else:
                    return jsonify(message = "Contraseña incorrecta", error = True), 401
          else:
               return jsonify(message = 'Usuario erroneo', error = True), 404
     else: return jsonify(message="Complete todos los campos", error = True), 400

#Crear tarea
@jwt_required()
def create(mysql):
     userData = get_jwt_identity()
     id_user = userData[1]
     title = request.json['title']
     description = request.json['description']
     if title and description :
          cur = mysql.connection.cursor()
          cur.execute('INSERT INTO tasks (id_user, title, description) VALUES (%s, %s, %s)', (id_user, title, description))
          mysql.connection.commit()
          return jsonify(message = "Nota creada con exito" ), 201
     else : 
          return jsonify(error = True), 404

#Obtener tareas
@jwt_required()
def get_tasks(mysql):
     userData = get_jwt_identity()
     id_user = str(userData[1])
     cur = mysql.connection.cursor()
     cur.execute('SELECT * FROM tasks WHERE id_user = %s', [id_user])
     tasks = cur.fetchall()
     mysql.connection.commit()
     return jsonify(tasks), 200

#Obtener una tarea
@jwt_required()
def get_id_tasks(id,mysql):
     userData = get_jwt_identity()
     id_user = str(userData[1])
     cur = mysql.connection.cursor()
     tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
     if tasks_user:
          task = cur.fetchall()
          mysql.connection.commit()
          return jsonify(task), 200
     else:
          return jsonify(error = True), 403

#Editar tarea
@jwt_required()
def edit_id_task(id, mysql):
     userData = get_jwt_identity()
     id_user = str(userData[1])
     cur = mysql.connection.cursor()
     tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
     if tasks_user:
          title= request.json['title']
          description= request.json['description']
          if title and description:
               cur.execute('UPDATE tasks SET title = %s, description = %s  WHERE tasks.id_task = %s',(title, description, id))
               mysql.connection.commit()
               return jsonify(message ='Datos actualizados correctamente'), 200
          else: 
               return jsonify(error = True), 404
     else:
          mysql.connection.commit()
          return jsonify(error = True), 403

#Eliminar tareas
@jwt_required()
def delete_id_task(id,mysql):
     userData = get_jwt_identity()
     id_user = str(userData[1])
     cur = mysql.connection.cursor()
     tasks_user = cur.execute('SELECT * FROM tasks WHERE id_user = %s and id_task = %s', (id_user, id))
     if tasks_user:
          cur.execute('DELETE FROM tasks WHERE tasks.id_task = %s', [id])
          mysql.connection.commit()
          return jsonify(), 204
     else:
          mysql.connection.commit()
          return jsonify(error = True), 403