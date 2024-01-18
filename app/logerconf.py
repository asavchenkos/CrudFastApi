from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .logger_config import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url}")

        # Log the request body
        body = await request.body()
        logger.info(f"Request body: {body}")

        # Call the next middleware and get the response
        response = await call_next(request)

        # Log the outgoing response
        logger.info(f"Outgoing response: {response.status_code}")

        # Create a copy of the response body
        response_body = b"".join([chunk async for chunk in response.__dict__['body_iterator']])

        # Log the response body
        logger.info(f"Response body: {response_body}")

        # Create a new response with the copied body
        new_response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

        return new_response