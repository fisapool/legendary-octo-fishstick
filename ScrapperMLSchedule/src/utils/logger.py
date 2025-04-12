import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = __name__,
    log_file: Optional[str] = "logs/a5.log",
    level: int = logging.INFO
) -> logging.Logger:
    """Configure and return a logger instance."""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Add file handler if log_file specified
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

def log_error(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """Log an error with context."""
    message = f"{context}: {str(error)}" if context else str(error)
    logger.error(message, exc_info=True)

def log_warning(logger: logging.Logger, message: str) -> None:
    """Log a warning message."""
    logger.warning(message)

def log_info(logger: logging.Logger, message: str) -> None:
    """Log an info message."""
    logger.info(message)
