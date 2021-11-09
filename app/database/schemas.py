# Paquetes
from ext import ma

class UserSchema(ma.Schema):
    class UsMeta:
        fields = ('id','username','password')

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_task' ,'title', 'description')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)