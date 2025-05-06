from pydantic import BaseModel
from typing import Optional

#Entidad user
class User(BaseModel): #BaseModel da la capacidad de crear una entidad para datos
    id: Optional[str] = None
    username: str
    email: str
