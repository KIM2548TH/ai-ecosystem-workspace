"""Legacy shim for utils.logger."""

from backend.app.utils.logger import (
    CustomJsonFormatter,
    JSONFormatter,
    generate_sample_logs,
    get_custom_logger,
    log_execution,
    log_fail,
    log_success,
    logger,
)

__all__ = [
    "CustomJsonFormatter",
    "JSONFormatter",
    "get_custom_logger",
    "logger",
    "log_success",
    "log_fail",
    "log_execution",
    "generate_sample_logs",
]
