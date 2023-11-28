from pathlib import Path


# Can not import this from Django settings because of circular import
# so need to create BASE_DIR here again
LOG_BASE_DIR = Path(__file__).resolve().parent.parent


CUSTOM_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },

    "formatters": {
        "console_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "console_warning_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{pathname} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "console_error_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{pathname} \n"
                      "{exc_info} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "file_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "file_warning_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{pathname} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "file_error_formatter": {
            "format": "[{asctime}] / {levelname} / {name} \n"
                      "{pathname} \n"
                      "{exc_info} \n"
                      "{message} \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },

    "handlers": {
        # DEBUG = True
        "info_console_debug_true": {
            "level": "INFO",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "console_formatter",
        },
        "warning_console_debug_true": {
            "level": "WARNING",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "console_warning_formatter",
        },
        "warning_file_debug_true": {
            "level": "WARNING",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_warning_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/debug/warning.log",
        },
        "error_console_debug_true": {
            "level": "ERROR",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "console_error_formatter",
        },
        "error_file_debug_true": {
            "level": "ERROR",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_error_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/debug/error.log",
        },
        "critical_console_debug_true": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "console_error_formatter",
        },
        "critical_file_debug_true": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_error_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/debug/critical.log",
        },

        # DEBUG = False
        "info_file_debug_false": {
            "level": "INFO",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/prod/info_prod.log",
        },
        "warning_file_debug_false": {
            "level": "WARNING",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_warning_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/prod/warning_prod.log",
        },
        "error_file_debug_false": {
            "level": "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_error_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/prod/error_prod.log",
        },
        "critical_file_debug_false": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "file_error_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/prod/critical_prod.log",
        },
    },

    "loggers": {
        "django.request": {
            "handlers": [
                "info_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": [
                "info_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [
                "info_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}
