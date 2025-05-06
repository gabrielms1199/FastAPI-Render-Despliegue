from pymongo import MongoClient

# Base de datos local
#db_client = MongoClient().local

# Base de datos remota
db_client = MongoClient("mongodb+srv://gabriel:1234@cluster0.x7fellu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test
#En cloud.mongodb.com se selecciona en el cluster creado: Connect -> Drivers -> Se pega la URL en la variable db_client

##URL para crear instancias y desplegar bases de datos remotamente (se puede elegir AWS): https://cloud.mongodb.com/
#Para conectarse a nuestro cluster de BD en VSCode, seleccionamos Connect -> MongoDB for VS Code -> Se pega la URL en un nuevo Connection String del plugin MongoDB de VSCode