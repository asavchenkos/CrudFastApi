import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

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