from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "c84cdf9ffb75f9e387180c1cc087a3d875d68ed342a745af2af87c7c3d889258" #Se genera con openssl rand -hex 32 

router = APIRouter() #Instanciamos FastAPI

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

#Instalar dependencias:
    #pip install "python-jose[cryptography]"
    #pip install "passlib[bcrypt]"

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User): 
    password: str


users_db = { 
    "gmoreno": {
        "username": "gmoreno",
        "full_name": "Gabriel Moreno",
        "email": "gmoreno@email.com",
        "disabled": False,
        "password": "$2a$12$cZ0vlNYG6CgQwGihgDUm7uadz.GdwojMa4o9bUC9h9ThsMD5W.mH." #Contraseña 123456 encriptada usando https://bcrypt-generator.com/
    },
    "gmoreno2": {
        "username": "gmoreno2",
        "full_name": "Gabriel Moreno 2",
        "email": "gmoreno@email.com",
        "disabled": True,
        "password": "$2a$12$WodLKrHjDoX97jajxba15uxuNWqqrBQbiMrQDQ3c0TZRUQEzKnkmi"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Se le pasan asteriscos para desempaquetar el diccionario y pasar sus claves como argumentos al constructor de UserDB
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # Se le pasan asteriscos para desempaquetar el diccionario y pasar sus claves como argumentos al constructor de UserDB


async def auth_user(token: str = Depends(oauth2)):
    exception= HTTPException(
        status_code=401, 
        detail="Credenciales de autenticación inválidas", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub") #https://jwt.io/
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=400, 
            detail="Usuario inactivo")
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400,
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password): #Se le pasan como parámetros la contraseña original y la contraseña encriptada
        raise HTTPException(
            status_code=400,
            detail="La contraseña no es correcta")

    access_token = {"sub":user.username,
                    "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


##Para hacer login con usuario, seleccionar en el New Request (tipo POST): Body -> Form -> username value gmoreno; password value 123456 (URL=http://127.0.0.1:8000/login)
##Luego se cambia a tipo GET y en URL=http://127.0.0.1:8000/users/me en Auth -> Bearer, ahí se pega el token que estamos usando