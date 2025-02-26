import os
from pathlib import Path
import colorlog

BASE_DIR = Path(__file__).resolve().parent.parent

log_dir = os.path.join(BASE_DIR, "logs")
log_file = os.path.join(BASE_DIR, log_dir, "django.log")


if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} - {name} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
        "colored": {
            "()": colorlog.ColoredFormatter,
            "format": "%(log_color)s[%(levelname)s] [%(asctime)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",  # Log only warnings and above to file
            "class": "logging.FileHandler",
            "filename": log_file,
            "formatter": "verbose",
        },
        "rotating_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "maxBytes": 5 * 1024 * 1024,  # 5 MB per file
            "backupCount": 3,  # Keep last 3 log files
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",  # Log debug and above to console
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "root": {  # This is the global logger for all Django apps
        "handlers": ["console", "rotating_file"],
        "level": "DEBUG",  # Log everything from DEBUG and above
    },
    "loggers": {
        "django": {  # Django's internal logs
            "handlers": ["console", "rotating_file"],
            "level": "INFO",
            "propagate": False,
        },
        # "django.db.backends": {  # Logs all SQL queries
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        "django.security": {  # Logs security-related messages
            "handlers": ["rotating_file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
