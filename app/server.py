"""
The common routine to set up FastAPI.
The main service application calls `setup_server` from this module.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.routes.health import router as health_router
from app.routes.nlip import router as nlip_router
from app.schemas import nlip

import random
import string

def create_app(client_app: nlip.NLIP_Application) -> FastAPI:
    @asynccontextmanager
    async def lifespan(this_app: FastAPI):
        # Startup logic
        client_app.startup()
        this_app.state.client_app = client_app
        this_app.state.client_app_session = client_app.create_session()

        if this_app.state.client_app_session:
            this_app.state.client_app_session.start()

        yield
        # Shutdown logic
        if this_app.state.client_app_session:
            this_app.state.client_app_session.stop()
            this_app.state.client_app_session = None

        client_app.shutdown()

    app = FastAPI(lifespan=lifespan)

    # Authlib.integrations.starlette_client.OAuth needs the Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key="".join(random.choice(string.ascii_letters) for _ in range(16)),
    )

    app.include_router(health_router, tags=["health"])
    # Include the NLIP routes
    app.include_router(nlip_router, prefix="/nlip", tags=["nlip"])

    return app


def setup_server(client_app: nlip.NLIP_Application) -> FastAPI:
    return create_app(client_app)
