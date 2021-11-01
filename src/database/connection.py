from flask_mysqldb import MySQL

def configureMySQL(app):
     app.config['MYSQL_HOST'] = '127.0.0.1'
     app.config['MYSQL_USER'] = 'root'
     app.config['MYSQL_PORT'] = '33061'
     app.config['MYSQL_PASSWORD'] = 'secret'
     app.config['MYSQL_DB'] = 'tareas'
     mysql = MySQL(app)
     return mysql


