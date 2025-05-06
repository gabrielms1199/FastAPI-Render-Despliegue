from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

#Usamos servidor uvicorn, y en @app.get especificamos la ruta a desplegar
#Arrancar servidor: uvicorn main:app --reload  (main nombre del fichero .py, y app de la instancia añadida)

#Documentación con Swagger UI si accedemos a https://127.0.0.1:8000/docs

#Instalar plugin Thunder Client en VSCode

app = FastAPI() #Instanciamos FastAPI

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)


#Recursos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static") #Para exponer recurso estático como imágenes

@app.get("/")
async def root(): #Esta función es asíncrona para que funcione y haga lo que tenga que hacer cuando pueda
    return "¡Hola FastAPI!"

@app.get("/url")
async def root(): #Esta función es asíncrona para que funcione y haga lo que tenga que hacer cuando pueda
    return { "url":"https://mouredev.com/python" }
