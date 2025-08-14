from fastapi import FastAPI
import logging
from logging.config import dictConfig
import sys
import json
from datetime import datetime


# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        # Add exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


# Define the logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json": {"()": JsonFormatter},
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "./logs/app.log",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
        },
        "time_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": "./logs/app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
        },
    },
    "loggers": {
        "src": {
            "handlers": [
                "console",
                "rotating_file",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "watchfiles.main": {
            "handlers": [],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {"handlers": ["rotating_file", "console"], "level": "INFO"},
}


def config():
    dictConfig(log_config)
