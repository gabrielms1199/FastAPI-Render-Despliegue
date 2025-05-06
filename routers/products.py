from fastapi import APIRouter

#Nueva API que hace referencia ahora a productos

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", 
                 "Producto 4", "Producto 5"]

@router.get("/") #Como este router con path "/" está dentro del prefijo *products, ya va a estar dentro, lo mismo con el router de path "/{id}"
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]