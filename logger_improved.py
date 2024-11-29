import logging
import os
from logging.config import dictConfig

def configure_logging():
    log_dir = "Logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Define logging configuration
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelname)s %(asctime)s [%(name)s] - %(message)s",
            },
            "detailed": {
                "format": "%(levelname)s %(asctime)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": os.path.join(log_dir, "app.log"),
                "formatter": "detailed",
                "level": "DEBUG",
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
    }

    # Apply logging configuration
    dictConfig(log_config)
