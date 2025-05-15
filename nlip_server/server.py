"""
The common routine to set up FastAPI.
The main service application calls `setup_server` from this module.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from nlip_server.routes.health import router as health_router
from nlip_server.routes.nlip import router as nlip_router
from nlip_sdk.nlip import NLIP_Message
from nlip_sdk import errors as err 
import secrets
import inspect

logger = logging.getLogger('uvicorn.error')

class NLIP_Session:
     
    def set_correlator(self):
        self.correlator = secrets.token_urlsafe()
    
    def get_correlator(self):
        if hasattr(self, "correlator"):
            return self.correlator
        return None

    def _print_withcorrelator(self, message:str):
        correlator = self.get_correlator()
        if correlator is not None:
            message = message + f" with correlator {self.correlator}"
        logger.info(message)

    def log_info(self, message:str):
        self._print_withcorrelator(message)
        
    async def start(self):
        self._print_withcorrelator("Session started")
        

    async def execute(self, msg: NLIP_Message) -> NLIP_Message:
        raise err.UnImplementedError("execute", self.__class__.__name__)
    
    async def correlated_execute(self, msg: NLIP_Message) -> NLIP_Message:
        # Check if the other side has sent a correlator 
        other_correlator =  msg.extract_conversation_token()
        rsp_or_coro = self.execute(msg)
        rsp = await rsp_or_coro if inspect.isawaitable(rsp_or_coro) else rsp_or_coro
        # There are three cases: 
        #  The other side has sent a correlator -- which is the one to send back
        #  The other side has not sent a correlator -- send one if set on local side
        #  The other side has not sent a correlator but subclass added a correlator -- do nothing

        existing_token = rsp.extract_conversation_token()
        if other_correlator is not None: 
            rsp.add_conversation_token(other_correlator,True)
        else:  
            if existing_token is None:
                local_correlator = self.get_correlator()
                if local_correlator is not None: 
                    logger.info("Adding Correlator ")
                    rsp.add_conversation_token(local_correlator)
        return rsp
 
    async def stop(self):
        self._print_withcorrelator("Session stopped")
    
    def get_logger(self):
        return logger
    

    



class NLIP_Application:
    async def startup(self):
        raise err.UnImplementedError(f"startup", self.__class__.__name__)

    async def shutdown(self):
        raise err.UnImplementedError(f"shutdown", self.__class__.__name__)

    def get_logger(self):
        return logger
    
    def create_session(self) -> NLIP_Session:
        raise err.UnImplementedError("create_session", self.__class__.__name__)
    
    def add_session(self, session_id:NLIP_Session) -> None:
        if hasattr(self, 'session_list'):
            if self.session_list is  None: 
                self.session_list = list()   
        else: 
            self.session_list = list()
        self.session_list.append(session_id)

    def remove_session(self, session_id:NLIP_Session) -> None:
        if hasattr(self, 'session_list'):
            self.session_list.remove(session_id)

class SafeApplication(NLIP_Application):
    
    async def startup(self):
        logger.info(f"Called startup on {self.__class__.__name__}")

    async def shutdown(self):
        logger.info(f"Called startup on {self.__class__.__name__}")
    
    



def create_app(client_app: NLIP_Application) -> FastAPI:
    @asynccontextmanager
    async def lifespan(this_app: FastAPI):
        # Startup logic
        startup_result = client_app.startup()
        if inspect.isawaitable(startup_result):
            await startup_result

        client_app.session_list = list()
        this_app.state.client_app = client_app

        yield

        # Shutdown logic
        for session in client_app.session_list:
            try:
                stop_result = session.stop()
                if inspect.isawaitable(stop_result):
                    await stop_result
            except Exception as e:
                logger.error(f'Exception {e} in trying to stop a session -- Ignored')

        client_app.session_list = list()

        shutdown_result = client_app.shutdown()
        if inspect.isawaitable(shutdown_result):
            await shutdown_result


    app = FastAPI(lifespan=lifespan)

    app.include_router(health_router, tags=["health"])
    # Include the NLIP routes
    app.include_router(nlip_router, prefix="/nlip", tags=["nlip"])
    
    return app


def setup_server(client_app: NLIP_Application) -> FastAPI:
    return create_app(client_app)
