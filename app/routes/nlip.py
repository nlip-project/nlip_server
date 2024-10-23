from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from app.schemas import nlip

router = APIRouter()


async def start_session(app):
    app.state.client_app_session = app.state.client_app.create_session()
    if app.state.client_app_session:
        app.state.client_app_session.start()


async def end_session(app):
    if app.state.client_app_session:
        app.state.client_app_session.stop()
    app.state.client_app_session = None


async def session_invocation(request: Request):
    app = request.app
    await start_session(app)
    try:
        if app.state.client_app_session is None:
            if app.state.client_app is not None:
                await start_session(app)
        yield app.state.client_app_session
    finally:
        await end_session(app)


@router.post("/")
async def chat_top(msg: nlip.NLIP_Message, session=Depends(session_invocation)):
    try:
        response = session.execute(msg)
        return response
    except nlip.NLIP_Exception as e:
        raise HTTPException(status_code=400, detail=nlip.nlip_encode_exception(e))


@router.post("/upload/")
async def upload(contents: Union[UploadFile, None] = None):
    filename = contents.filename if contents else "No file parameter"
    return nlip.nlip_encode_text(f"File {filename} uploaded successfully")
