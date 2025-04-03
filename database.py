from beanie import init_beanie, Document
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4, UUID
from datetime import datetime
from os import getenv
from pydantic import Field, BaseModel
DB_ENVIRONMENT_VAR = 'MONGO_URI'

class Product(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: Optional[int] = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UpdatedProduct(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    category: Optional[str] = Field(default=None)
    stock: Optional[int] = Field(default=None)

class SearchCriteria(BaseModel):
    search: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    min_price: Optional[float] = Field(default=0.0)
    max_price: Optional[float] = Field(default=1000.0)
    min_stock: Optional[int] = Field(default=0)
    max_stock: Optional[int] = Field(default=500)

def get_environment() -> None:
    env: str = getenv(DB_ENVIRONMENT_VAR)

    if env == None:
        # Error de sistema en caso de no encontrar una variable de entorno
        raise SystemError(f"Couldn't find environment variable {DB_ENVIRONMENT_VAR}")

    return env

async def init() -> None:
    # Cliente
    client = AsyncIOMotorClient(
        get_environment()
    )

    await init_beanie(database=client.db_name, document_models=[Product])

if __name__ == "__main__":
    # Propósitos de testeo
    pass