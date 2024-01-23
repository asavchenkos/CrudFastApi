import logging
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url}")

        # Log the request body
        body = await request.body()
        logger.info(f"Request body: {body.decode()}")

        # Call the next middleware and get the response
        response = await call_next(request)

        # Create a copy of the response body
        response_body = b"".join([chunk async for chunk in response.__dict__['body_iterator']])

        # Log the response body along with the response status code
        logger.info({"Response code": response.status_code, "Response body": response_body.decode()})

        # Create a new response with the copied body
        new_response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

        return new_response


class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Let the base class do its formatting
        super().format(record)

        # Now, record.asctime is available
        log_message = {
            "time": record.asctime,
            "Logger": record.name,
            "Level": record.levelname,
            "Message": record.getMessage(),
        }
        if isinstance(record.msg, dict):
            log_message.update(record.msg)  # Add the additional fields to the log message

        return json.dumps(log_message, separators=(',', ':'), indent=None)

# Create a logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a TimedRotatingFileHandler
# The logs will be stored in a 'logs' folder at the root of the project
# The filename will include the current date and have a .json extension
handler = TimedRotatingFileHandler(f"logs/my_log_{current_date}.json", when="midnight", backupCount=30)

# Set the log format to JsonFormatter
formatter = JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
