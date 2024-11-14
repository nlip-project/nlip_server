from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from app.schemas import nlip

router = APIRouter()

from fastapi.security.open_id_connect_url import OpenIdConnect
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
from fastapi import Request
from fastapi import Depends
from fastapi import status
import string
import random
from typing import Optional

oicd_discovery_url = "http://127.0.0.1:9000/o/.well-known/openid-configuration"

OIDC_config = {
    "client_id" : "swaggerclient",
    "base_authorization_server_uri": "http://127.0.0.1:9000/o",
    "issuer": "Me",
    "signature_cache_ttl": 3600,
}

authlib_oauth = OAuth()
authlib_oauth.register(
    name="myapp",
    server_metadata_url=oicd_discovery_url,
    client_kwargs={"scope": "openid email read write profile"},
    #client_id="some-client-id", # if enabled, authlib will also check that the access token belongs to this client id (audience)
)

fastapi_oauth2 = OpenIdConnect(
    openIdConnectUrl=oicd_discovery_url,
    scheme_name="My Authentification Method",
)

# The implementation of the check was inspired by this reference
#   https://github.com/HarryMWinters/fastapi-oidc/issues/1
# The swagger interface is retrieving an auth token ("token") and not
# a JWT identity token ("id_token").  So we query the /userinfo endpoint
# of the Authentication server to get the user details andd claims.

async def current_user(
    request: Request, token: Optional[str] = Depends(fastapi_oauth2)
):
    # we query the identity provider to give us some information about the user.
    # If this succeeds, we consider the user authenticated.
    # NOTE: for the NLIP demo, Swagger has passed the token as a string in the form of
    #    Bearer xyzxyzxyz
    # Authlib wants just the xyzxyzxyz part because it adds the prefix "Bearer ".
    # Here, we split the token and pass just the tok_part.
    # print(f"TOKEN:{token}")
    bear_part, tok_part = token.split(" ")
    # print(f"BEAR:{bear_part} TOK:{tok_part}")
    userinfo = await authlib_oauth.myapp.userinfo(token={"access_token": tok_part})
    print(f"USERINFO:{userinfo}")
    return token

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

# 
@router.post("/")
async def chat_top(msg: nlip.NLIP_BasicMessage | nlip.NLIP_Message, session=Depends(session_invocation), token: str = Depends(current_user)):
    try:
        response = session.execute(msg)
        print(f"Token {token}")
        return response
    except nlip.NLIP_Exception as e:
        raise HTTPException(status_code=400, detail=nlip.nlip_encode_exception(e))


@router.post("/upload/")
async def upload(contents: Union[UploadFile, None] = None):
    filename = contents.filename if contents else "No file parameter"
    return nlip.nlip_encode_text(f"File {filename} uploaded successfully")
