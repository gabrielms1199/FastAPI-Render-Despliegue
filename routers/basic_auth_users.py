from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter() #Instanciamos FastAPI

oauth2 = OAuth2PasswordBearer(tokenUrl="login-basic")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User): #Tiene todo lo del usuario anterior, más el password
    password: str

users_db = { #Representa BD no relacional, usando lista/array de diferentes usuarios
    "gmoreno": {
        "username": "gmoreno",
        "full_name": "Gabriel Moreno",
        "email": "gmoreno@email.com",
        "disabled": False,
        "password": "123456"
    },
    "gmoreno2": {
        "username": "gmoreno2",
        "full_name": "Gabriel Moreno 2",
        "email": "gmoreno@email.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Se le pasan asteriscos para desempaquetar el diccionario y pasar sus claves como argumentos al constructor de UserDB
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # Se le pasan asteriscos para desempaquetar el diccionario y pasar sus claves como argumentos al constructor de UserDB

    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Credenciales de autenticación inválidas", 
            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=400, 
            detail="Usuario inactivo")
    return user



@router.post("/login-basic")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400,
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400,
            detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


