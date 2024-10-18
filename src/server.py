'''
The common routine to setup fastAPI 

The main service application do do a call to setup_server of this module. 


'''
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, Depends
from typing import Union 
from src import nlip

def setup_server(client_app:nlip.NLIP_Application):

    @asynccontextmanager
    async def lifespan(this_app: FastAPI):
        client_app.startup()
        yield
        client_app.shutdown()

    app = FastAPI(lifespan=lifespan)

    async def start_session():
        app.state.client_app_session = client_app.create_session()
        if app.state.client_app_session is not None: 
            app.state.client_app_session.start()

    async def end_session():
        if app.state.client_app_session is not None: 
            app.state.client_app_session.stop()
        app.state.client_app_session = None

    async def session_invocation():
        await start_session()
        try:
            if app.state.client_app_session is None: 
                if client_app is not None: 
                    app.state.client_app_session = client_app.create_session()
                    if app.state.client_app_session is not None:
                        app.state.client_app_session.start()
            yield app.state.client_app_session 
        finally:
            await end_session()

    @app.post("/nlip/")
    async def chat_top(msg:nlip.NLIP_Message, session=Depends(session_invocation)):
        try:
            response = app.state.client_app_session.execute(msg)
            return response 
        except nlip.NLIP_Exception as e:
            return nlip.nlip_encode_exception(e)

    @app.post("/upload/")
    async def upload(contents:Union[UploadFile, None] = None):
        filename = "No file parameter"
        if contents is not None: 
            filename=contents.filename 
        return nlip.nlip_encode_text(f'File {filename} uploaded successfully')


    return app