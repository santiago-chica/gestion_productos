from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
from database import Product, UpdatedProduct, init
from datetime import datetime
from uuid import UUID

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
    await product.insert()

    return product.model_dump()

# Obtener todos los productos con paginación y filtro de búsqueda por nombre o categoría.
@app.get(f"/{ENDPOINT_NAME}")
async def obtain_product():
    return {"Hello world!!": True}

# Obtener producto por id
@app.get(f"/{ENDPOINT_NAME}/{{item_id}}")
async def obtain_product(item_id: str):
    uuid: UUID

    try:
        uuid = UUID(item_id)
    except Exception:
        return {"success": False, "message": "No es una UUID válida"}


    product = await Product.get(uuid)

    if product == None:
        return {"success": False, "message": "El producto no existe"}

    return product.model_dump()

# Actualizar producto
@app.put(f"/{ENDPOINT_NAME}/{{item_id}}")
async def update_product(item_id: str, updated_product: UpdatedProduct):
    uuid: UUID

    try:
        uuid = UUID(item_id)
    except Exception:
        return {"success": False, "message": "No es una UUID válida"}
    
    database_product = await Product.get(uuid)

    if database_product == None:
        return {"success": False, "message": "El producto no existe"}

    for k, v in updated_product.model_dump().items():
        if v == None:
            continue

        await database_product.update({'$set': {k: v}})

    database_product.updated_at = datetime.now()

    await database_product.save()
    
    return database_product.model_dump()

# Eliminar producto
@app.delete(f"/{ENDPOINT_NAME}/{{item_id}}")
async def delete_product(item_id: str):
    uuid: UUID

    try:
        uuid = UUID(item_id)
    except Exception:
        return {"success": False, "message": "No es una UUID válida"}
    
    product = await Product.get(uuid)

    if product == None:
        return {'success': False, 'message': 'El producto no existe'}
    
    await product.delete()

    return {"success": True, 'deleted_product': product.model_dump()}