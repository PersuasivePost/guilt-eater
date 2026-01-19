import os
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from starlette.requests import Request

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

oauth = OAuth()

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


async def get_google_user(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = await oauth.google.parse_id_token(request, token)
    return userinfo
