from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from db import database
import mqtt

from routers import devices, commands, admin, config
import connections


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.setup()
    mqtt.setup(asyncio.get_event_loop())
    yield


app = FastAPI(
    lifespan=lifespan,
    title="TPHome API",
    root_path="/api"
)

app.include_router(connections.router)
app.include_router(commands.router)
app.include_router(devices.router)
app.include_router(config.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)