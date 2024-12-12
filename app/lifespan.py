from contextlib import asynccontextmanager

from fastapi import FastAPI
from models import close_orm, init_orm


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await close_orm()