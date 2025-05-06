## Users DB API ##

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter()

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


#Path
@router.get("/{id}") #Para llamar a un usuario concreto con su propia id como parámetro
async def user(id: str):
    return search_user("_id", ObjectId(id))


#Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    else:
        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user)

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


@router.put("/", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    

#Arrancar BD MongoDB:
#.\mongod.exe --dbpath=E:\Documentos\CursoPythonPrincipiante\mongodb-win32-x86_64-windows-8.0.8\data

#Conexión en plugin MongoDB de VS Code: mongodb://localhost

#Colocar en un nuevo request esto en Body para añadir usuario de ejemplo:
    #{"username": "gmoreno", "email": "gmoreno@email.com"}