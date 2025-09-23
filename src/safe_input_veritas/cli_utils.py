"""
cli_utils - Utilities for command-line interface interactions with logging.

This module provides utility functions to enhance command-line interface
experiences for SafeInputVeritas users, integrating consistent logging and
internationalized messaging.

Functions include user prompts for pausing, printing informative messages,
and reading choices with validation.
"""

from __future__ import annotations

from safe_input_veritas.logger_config.logger_setup import (
    get_logger,
    get_message,
)

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-stable"

logger = get_logger()


def pause_prompt() -> None:
    """
    Display a prompt asking the user to press Enter to continue.

    Logs the pause event and waits for user input without echoing.

    Usage:
        Call this function when you want to pause CLI execution
        until the user decides to continue.

    Returns:
        None
    """
    logger.info("Pausing execution, waiting for user to continue.")
    input(get_message("pause_prompt"))


def print_info(message_key: str) -> None:
    """
    Print an informational message to the CLI, fetched from localized messages.

    Args:
        message_key (str): The key to retrieve the localized message.

    Usage:
        Use where CLI information messages are needed with support
        for multiple languages.

    Returns:
        None
    """
    message = get_message(message_key)
    logger.info("INFO: %s", message)
    print(message)


def print_error(message_key: str) -> None:
    """
    Print an error message to the CLI, fetched from localized messages.

    Args:
        message_key (str): The key to retrieve the localized error message.

    Usage:
        Use when CLI error messages need to be displayed and logged with
        proper internationalization.

    Returns:
        None
    """
    message = get_message(message_key)
    logger.error("ERROR: %s", message)
    print(message)
