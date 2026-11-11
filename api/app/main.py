from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from db import database
import mqtt

from routers import devices, commands, admin, config, firmware, logs
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
app.include_router(firmware.router)
app.include_router(logs.router)
