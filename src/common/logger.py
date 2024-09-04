import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Create the 'logs' directory if it doesn't exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Define the TimedRotatingFileHandler with the base filename
log_file_base = os.path.join(log_directory, "log")


# Define the custom logging handler
class CustomHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        self.callback(message, record.levelname)


# Create a TimedRotatingFileHandler that creates a new file every day
handler = TimedRotatingFileHandler(
    log_file_base, when="midnight", interval=1, backupCount=100
)
handler.suffix = "%Y%m%d.log"

# Define the log format
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s - %(message)s", datefmt="%H:%M:%S"
)
handler.setFormatter(formatter)

# Create the logger
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Optional: Log to console as well
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
