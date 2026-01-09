"""
Logging configuration.
"""

import logging
import sys


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    return logging.getLogger("jira-ai-agent")


# Global logger instance
logger = setup_logging()
