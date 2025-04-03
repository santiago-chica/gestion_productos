from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Product, init

ENDPOINT_NAME: str = "products"

# Inicialización
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield

app:FastAPI = FastAPI(lifespan=lifespan)

# Creación del producto
@app.post(f"/{ENDPOINT_NAME}")
async def create_product(product: Product):
    product.insert()

    return product.model_dump()

# Obtener todos los productos con paginación y filtro de búsqueda por nombre o categoría.
@app.get(f"/{ENDPOINT_NAME}")
async def obtain_product():
    return {"Hello world!!": True}

# Obtener producto por id
@app.get(f"/{ENDPOINT_NAME}/{{item_id}}")
async def obtain_product():
    return {"Hello world!!": True}

# Actualizar producto
@app.put(f"/{ENDPOINT_NAME}/{{item_id}}")
async def update_product():
    return {"Hello world!!": True}

# Eliminar producto
@app.delete(f"/{ENDPOINT_NAME}/{{item_id}}")
async def delete_product():
    return {"Hello world!!": True}