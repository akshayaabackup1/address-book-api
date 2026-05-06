import logging

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Address Book API",
    description="Simple address book with CRUD and distance-based search.",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    # create tables if they don't exist yet
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("App started, database is ready.")


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Address Book API is running"}
