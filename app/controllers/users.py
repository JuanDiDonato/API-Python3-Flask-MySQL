# Modulos
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies

# Paquetes
from helpers import bcrypt
from database.models import Task, Users 
from database.schemas import user_schema, task_schema, tasks_schema, users_schema

#Registrar usuario
def addUser(db):
     username = request.json['username']
     password = request.json['password']
     if username and password:
          user_data = db.session.query(Users).filter_by(username=username).first()
          if user_data:
               return jsonify(message="Nombre de usuario ya en uso", error=True), 404
          password = bcrypt.hashPassword(password)
          new_user = Users(username,password)
          db.session.add(new_user)
          db.session.commit()
          return user_schema.jsonify(new_user), 201
     else : return jsonify(message="Complete todos los campos", error=True), 404

#Loguear usuario
def loginUser(db):
     user_name = request.json['username']
     password = request.json['password']
     if password and user_name :
          password = password.encode()
          user_data = db.session.query(Users).filter_by(username=user_name).first()
          if user_data:
               password_db, id, username = user_data.password, user_data.id, user_data.username
               user = (id,username)
               password_db = password_db.encode()
               check_password = bcrypt.comparePassword(password, password_db)
               print(check_password)
               if check_password:
                    response = jsonify(isAuth = True)
                    access_token = create_access_token(identity=[user,id])
                    set_access_cookies(response, access_token)
                    return response,200
                    # return jsonify(token = access_token, isAuth = True), 200
                    #En el frontend, para podes verificar la cookie, en la consulta a una ruta
                    #se debe agregar el header:
                    # headers: {
                    # 'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                    # },
               else:
                    return jsonify(message = "Datos no validos.", error = True), 401
          else:
               return jsonify(message = 'Usuario erroneo', error = True), 404
     else: return jsonify(message="Complete todos los campos", error = True), 400 

#Logout
def clearCookie():
     response = jsonify({"msg": "logout successful"})
     unset_jwt_cookies(response)
     return response, 200

#Crear tarea
@jwt_required()
def create(db):
     userData = get_jwt_identity()
     id = userData[1]
     title = request.json['title']
     description = request.json['description']
     if title and description:
          new_task = Task(title, description, id)
          db.session.add(new_task)
          db.session.commit()
          return jsonify(message="Nota agregada", error=False), 201
     else : return jsonify(message="Complete todos los campos", error = True),404

#Obtener tareas
@jwt_required()
def get_tasks(db):
     userData = get_jwt_identity()
     id_user = str(userData[1])
     tasks = db.session.query(Task).filter_by(id=id_user).all()
     db.session.commit()
     return tasks_schema.jsonify(tasks), 200

#Obtener una tarea
@jwt_required()
def get_id_tasks(id,db):
     userData = get_jwt_identity()
     id_user = userData[1]
     task = db.session.query(Task).filter_by(id_task = id , id = id_user).first()
     db.session.commit()
     if task:
          return task_schema.jsonify(task), 200
     else:
          return jsonify(error=True), 403

#Editar tarea
@jwt_required()
def edit_id_task(id, db):
     userData = get_jwt_identity()
     id_user = userData[1]
     task = db.session.query(Task).filter_by(id_task = id , id = id_user).first()

     if task:
          task.title = request.json['title']
          task.description= request.json['description']
          db.session.commit()
          return jsonify(message ='Datos actualizados correctamente'), 200
     else:
          db.connection.commit()
          return jsonify(error = True), 403

#Eliminar tareas
@jwt_required()
def delete_id_task(id,db):
     userData = get_jwt_identity()
     id_user = userData[1]
     task = db.session.query(Task).filter_by(id_task = id , id = id_user).first()

     if task:
          db.session.delete(task)
          db.session.commit()
          return jsonify(message ='Datos borrados con exito'), 200
     else:
          db.connection.commit()
          return jsonify(error = True), 403