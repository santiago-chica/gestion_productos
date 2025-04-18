from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import Product, UpdatedProduct
from database import init as start_database
from datetime import datetime
from uuid import UUID

MAX_LEVENSHTEIN_DISTANCE: int = 10
ENDPOINT_NAME: str = "products"

# Inicialización
@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_database()
    yield

app = FastAPI(lifespan=lifespan)

# Creación del producto
@app.post(f"/{ENDPOINT_NAME}")
async def create_product(product: Product):
    if product.stock < 0:
        raise HTTPException(status_code=500, detail="El stock no puede ser negativo")
    if product.price < 0:
        raise HTTPException(status_code=500, detail="El precio no puede ser negativo")

    await product.insert()

    return product.model_dump()

# Valores por defecto
MIN_PRICE:float = 0.0
MAX_PRICE:float = 50_000.0
MIN_STOCK:int = 0
MAX_STOCK:int = 1000
SKIP:int = 0
LIMIT:int = 10

# Obtener todos los productos con paginación y filtro de búsqueda por nombre o categoría.
@app.get(f"/{ENDPOINT_NAME}")
async def obtain_product(
    search: str = None,
    category: str = None,
    min_price:float = MIN_PRICE,
    max_price:float = MAX_PRICE,
    min_stock:int = MIN_STOCK,
    max_stock:int = MAX_STOCK,
    skip:int = SKIP,
    limit:int = LIMIT):

    conditions = [
        min_price <= Product.price <= max_price,
        min_stock <= Product.stock <= max_stock
    ]

    if search != None:
        conditions.append(Product.name == search)
    if category != None:
        conditions.append(Product.category == category)
    

    product_list = await Product.find(
        *conditions,
        skip=skip,
        limit=limit
    ).to_list()

    if len(product_list) == 0:
        return HTTPException(status_code=404, detail="Sin datos encontrados")

    return product_list

# Obtener producto por id
@app.get(f"/{ENDPOINT_NAME}/{{item_id}}")
async def obtain_product_id(item_id: str):
    uuid: UUID

    try:
        uuid = UUID(item_id)
    except Exception:
        raise HTTPException(status_code=500, detail="No es una UUID válida")


    product = await Product.get(uuid)

    if product == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

    return product.model_dump()

# Actualizar producto
@app.put(f"/{ENDPOINT_NAME}/{{item_id}}")
async def update_product(item_id: str, updated_product: UpdatedProduct):
    if updated_product.stock != None and updated_product.stock < 0:
        raise HTTPException(status_code=500, detail="El stock no puede ser negativo")
    if updated_product.price != None and updated_product.price < 0:
        raise HTTPException(status_code=500, detail="El precio no puede ser negativo")

    uuid: UUID

    try:
        uuid = UUID(item_id)
    except Exception:
        raise HTTPException(status_code=500, detail="No es una UUID válida")
    
    database_product = await Product.get(uuid)

    if database_product == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

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
        raise HTTPException(status_code=500, detail="No es una UUID válida")
    
    product = await Product.get(uuid)

    if product == None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    
    await product.delete()

    return {"success": True, 'deleted_product': product.model_dump()}