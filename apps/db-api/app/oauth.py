from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.common.security import generate_token

from litestar import Litestar, get, Request
from litestar.datastructures import State

from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# Separate asyncontextmanager for each IdP

GOOGLE_AUTHORIZATION_ENDPOINT='https://accounts.google.com/o/oauth2/v2/auth'

@asynccontextmanager
async def google_oauth_client(app: Litestar) -> AsyncGenerator[None, None]:
    client: AsyncOAuth2Client = getattr(app.state, 'google_oauth_client', None)
    if client is None:
        client = AsyncOAuth2Client(
            client_id=GOOGLE_CLIENT_ID ,
            client_secret=GOOGLE_CLIENT_SECRET,
            # We don't need "email", but Google requires it or "profile"
            # https://developers.google.com/identity/openid-connect/openid-connect#scope-param
            scope='openid email',
        )

    try:
        yield
    finally:
        await client.aclose()


@get('/login/google')
async def google_login(state: State, request: Request):
    client: AsyncOAuth2Client = state.google_oauth_client
    nonce = generate_token()
    print(request.session)
    # i don't think this session stuff works
    request.set_session({'nonce': nonce})
    client.create_authorization_url(
        url=GOOGLE_AUTHORIZATION_ENDPOINT,
        redirect_uri=request.url_for('google_auth'),
        nonce=nonce,
    )

@get('/auth/google')
async def google_auth():
    ...
