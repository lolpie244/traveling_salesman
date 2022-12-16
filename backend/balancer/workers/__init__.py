from fastapi import FastAPI

from .nearest import router as nearest_router


def attach_routers(app: FastAPI):
    app.mount("/solver", nearest_router)

