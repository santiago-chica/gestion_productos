from beanie import init_beanie, Document
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4, UUID
from datetime import datetime
from os import getenv
from pydantic import Field
DB_ENVIRONMENT_VAR = 'MONGO_URI'

class Product(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: Optional[int] = 0
    #created_at: datetime
    #updated_at: datetime

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