from typing import Union
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from nlip_sdk import nlip

router = APIRouter()
logger = logging.getLogger('uvicorn.error')

async def start_session(request: Request):
    logger.info('Called start_session')
    app = request.app
    if app.state.client_app:
        if not hasattr(request.state, 'nlip_session'):  
            request.state.nlip_session = app.state.client_app.create_session()
            request.state.nlip_session.start()
            app.state.client_app.add_session(request.state.nlip_session)
            logger.info('Called nlip_session.start')



async def end_session(request: Request):
    if request.app.state.client_app:
        request.app.state.client_app.remove_session(request.state.nlip_session)

    if hasattr(request.state, 'nlip_session'):
        request.state.nlip_session.stop()
        logger.info('Called nlip_session.stop')
    request.state.nlip_session = None


async def session_invocation(request: Request):
    if not hasattr(request.state, 'nlip_session'): 
        await start_session(request)
    try:
        yield request.state.nlip_session
    finally:
        await end_session(request)


@router.post("/")
async def chat_top(msg: nlip.NLIP_BasicMessage | nlip.NLIP_Message, session=Depends(session_invocation)):
    try:
        response = session.execute(msg)
        return response
    except nlip.Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/")
async def upload(contents: Union[UploadFile, None] = None):
    filename = contents.filename if contents else "No file parameter"
    return nlip.nlip_encode_text(f"File {filename} uploaded successfully")
