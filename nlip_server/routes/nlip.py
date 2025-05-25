from typing import Union
import logging
import inspect

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from nlip_sdk import nlip

router = APIRouter()
logger = logging.getLogger('uvicorn.error')

async def start_session(request: Request):
    logger.info('Called start_session')
    app = request.app

    if app.state.client_app and not hasattr(request.state, 'nlip_session'):
        session = app.state.client_app.create_session()
        if inspect.isawaitable(session):
            session = await session
        request.state.nlip_session = session

        start_result = session.start()
        if inspect.isawaitable(start_result):
            await start_result

        app.state.client_app.add_session(session)
        logger.info('Called nlip_session.start')



async def end_session(request: Request):
    if request.app.state.client_app:
        request.app.state.client_app.remove_session(request.state.nlip_session)

    if hasattr(request.state, 'nlip_session'):
        stop_result = request.state.nlip_session.stop()
        if inspect.isawaitable(stop_result):
            await stop_result
        logger.info('Called nlip_session.stop')

    request.state.nlip_session = None



async def session_invocation(request: Request):
    if not hasattr(request.state, 'nlip_session'):
        await start_session(request)
    try:
        yield request.state.nlip_session
    finally:
        await end_session(request)

import traceback
import sys

@router.post("/")
async def chat_top(msg: nlip.NLIP_Message, session=Depends(session_invocation)):
    try:
        response = await session.correlated_execute(msg)
        return response
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/")
async def upload(contents: Union[UploadFile, None] = None):
    filename = contents.filename if contents else "No file parameter"
    return nlip.NLIP_Factory.create_text(f"File {filename} uploaded successfully")
