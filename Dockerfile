#Sistema
FROM ubuntu:20.04

#Python3 y Pip
RUN apt update && apt upgrade 
RUN apt install python3 -y
RUN apt install pip -y
RUN apt install libmysqlclient-dev -y
RUN apt install libmariadb-dev-compat -y
RUN apt install libmariadbclient-dev -y



#Creo una carpeta app donde copiare mi proyecto
WORKDIR /flask-rest-api
#Selecciono todo el proyecto (con el .) y lo copio a app
COPY . /flask-rest-api
#Instala los modulos necesarios desde requirements.txt
RUN pip --no-cache-dir install -r requirements.txt
#Inicio la app
CMD ["python3", "src/app.py"]