from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from core.services.jwt_service import JWTService, SocketToken


@database_sync_to_async
def get_user(token: str | None):
    if not token:
        return None
    try:
        return JWTService.verify_token(token, SocketToken)
    except Exception:
        return None


class AuthSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode('utf8')
        query_params = parse_qs(query_string)

        token = query_params.get('token', [None])[0]

        scope['user'] = await get_user(token=token)

        return await super().__call__(scope, receive, send)