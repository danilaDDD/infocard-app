from datetime import datetime

import jwt
from django.conf import settings

from apps.account.models import Account
from settings.settings import JWT_ALGORITHM

TYPE_ACCESS_TOKEN = 'access'
TYPE_REFRESH_TOKEN = 'refresh'

def decode_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        decoded['expired_at'] = datetime.fromtimestamp(decoded.get('exp'))
        decoded['user_id'] = int(decoded.get('user_id'))

        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def check_jwt(token: str, account: Account, type: str) ->bool:
    try:
        decoded = decode_jwt(token)
        return (decoded['token_type'] == type
         and decoded['user_id'] == account.id and decoded['expired_at'] > datetime.now())

    except ValueError:
        return False

