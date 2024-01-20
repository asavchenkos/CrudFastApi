import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Create a logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a TimedRotatingFileHandler
# The logs will be stored in a 'logs' folder at the root of the project
# The filename will include the current date
handler = TimedRotatingFileHandler(f"logs/my_log_{current_date}.log", when="midnight", backupCount=30)

# Set the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

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