from fastapi import FastAPI

ENDPOINT_NAME: str = "products"

app:FastAPI = FastAPI()

# Creación del producto
@app.post(f"/{ENDPOINT_NAME}/")
def create_product():
    return {"Hello world!!": True}

# Obtener todos los productos con paginación y filtro de búsqueda por nombre o categoría.
@app.get(f"/{ENDPOINT_NAME}/")
def obtain_product():
    return {"Hello world!!": True}

# Actualizar producto
@app.put(f"/{ENDPOINT_NAME}/")
def update_product():
    return {"Hello world!!": True}

# Eliminar producto
@app.delete(f"/{ENDPOINT_NAME}/")
def delete_product():
    return {"Hello world!!": True}