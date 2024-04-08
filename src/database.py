from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)
