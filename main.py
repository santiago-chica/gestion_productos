from pydantic import BaseModel
from fastapi import FastAPI
from uuid import uuid4, UUID
from datetime import datetime
from datetime import datetime

app = FastAPI()

class Product(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    category: str
    stock: int
    created_at: datetime
    updated_at: datetime

# Creación del producto
@app.get("/")
def test():
    return {"Hello world!!": True}