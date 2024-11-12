"""
The common routine to set up FastAPI.
The main service application calls `setup_server` from this module.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from nlip_server.routes.health import router as health_router
from nlip_server.routes.nlip import router as nlip_router
from nlip_sdk.nlip import NLIP_BasicMessage, NLIP_Message
from nlip_sdk import errors as err 

logger = logging.getLogger('uvicorn.error')

class NLIP_Session:
    def start(self):
        raise err.UnImplementedError("start", self.__class__.__name__)

    def execute(self, msg: NLIP_Message | NLIP_BasicMessage) -> NLIP_Message | NLIP_BasicMessage:
        raise err.UnImplementedError("execute", self.__class__.__name__)
 
    def stop(self):
        raise err.UnImplementedError("stop", self.__class__.__name__)
    
    def get_logger(self):
        return logger
    



class NLIP_Application:
    def startup(self):
        raise err.UnImplementedError("startup", self.__class__.__name__)

    def shutdown(self):
        raise err.UnImplementedError("shutdown", self.__class__.__name__)

    def get_logger(self):
        return logger
    
    def create_session(self) -> NLIP_Session:
        raise err.UnImplementedError("create_session", self.__class__.__name__)
    
    def add_session(self, session_id:NLIP_Session) -> None:
        if hasattr(self, 'session_list'):
            self.session_list.append(session_id)
        else: 
            self.session_list = list()
            self.session_list.append(session_id)

    
    def remove_session(self, session_id:NLIP_Session) -> None:
        if hasattr(self, 'session_list'):
            self.session_list.remove(session_id)


def create_app(client_app: NLIP_Application) -> FastAPI:
    @asynccontextmanager
    async def lifespan(this_app: FastAPI):
        # Startup logic
        client_app.startup()
        client_app.session_list = list()
        this_app.state.client_app = client_app

        yield
        # Shutdown logic
        for session in client_app.session_list:
            try:
                session.stop()
            except Exception as e:
                logger.error(f'Exception {e} in trying to stop a session -- Ignored') 

        client_app.session_list = list()
        client_app.shutdown()

    app = FastAPI(lifespan=lifespan)

    app.include_router(health_router, tags=["health"])
    # Include the NLIP routes
    app.include_router(nlip_router, prefix="/nlip", tags=["nlip"])
    
    return app


def setup_server(client_app: NLIP_Application) -> FastAPI:
    return create_app(client_app)
