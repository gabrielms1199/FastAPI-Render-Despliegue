from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

#Arrancar servidor: uvicorn users:app --reload  (main nombre del fichero .py, y app de la instancia añadida)
#127.0.0.1:8000/ruta

#Entidad user
class User(BaseModel): #BaseModel da la capacidad de crear una entidad para datos
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Gabriel", surname="Moreno", url="https://gmoreno.dev", age=25),
              User(id=2, name="Moure", surname="Dev", url="https://moure.dev", age=35),
              User(id=3, name="Haakon", surname="Dahlberg", url="https://haakon.com", age=33)]



@router.get("/usersjson")
async def usersjson():
    return [{"name":"Gabriel", "surname":"Moreno", "url":"https://gmoreno.dev", "age":25},
            {"name":"Moure", "surname":"Dev", "url":"https://moure.dev", "age": 35},
            {"name":"Haakon", "surname":"Dahlberg", "url":"https://haakon.com", "age": 33}]


@router.get("/users")
async def users():
    return users_list


#Path
@router.get("/user/{id}") #Para llamar a un usuario concreto con su propia id como parámetro
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list) #Para buscar por id de usuario
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    

#Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)


@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user
"""
Se debe colocar en JSON Content en "Body" el formato de campos de user en JSON para agregar un nuevo usuario, y hacer el request de POST para agregarlo.
Ejemplo:
{
  "id": 4,
  "name": "Gabriel",
  "surname": "Moreno",
  "url": "https://gmoreno.dev",
  "age": 25
}
"""


@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user
    

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True   
    if not found:
        return {"error": "No se ha eliminado el usuario"}
#La operación DELETE ignora lo que se pase por JSON en el content de debajo, ya que solo tiene en cuenta el id del usuario que se le pase en el path

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) 
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}