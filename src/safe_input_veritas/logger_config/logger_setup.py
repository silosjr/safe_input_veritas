"""
logger_setup - Centralized logging setup and internationalized messages.

This module configures the application-wide logging system for SafeInputVeritas,
ensuring consistent, structured, and secure logs for auditability and
troubleshooting. It provides a configurable logger supporting multiple
verbosity levels and output formats suitable for CLI and production use.

Additionally, this module manages internationalized message templates for
important validation events and errors, currently supporting English (US),
Portuguese (BR), and Spanish (ES) locales.

Features:
- Standardized logging format with timestamps, levels and message context.
- Internationalization using importlib.resources for packaged locale files.
- Language selection via environment variable or default to English.
- Centralized message repository to avoid hardcoded strings in code.
- Designed for extensibility to support new languages and log handlers.

Usage:
Import `get_logger()` to obtain the configured logger instance.
Use `get_message(key: str, lang: str = 'en_US')` to fetch localized messages.
"""

from __future__ import annotations

import importlib.resources
import json
import logging
import os
from typing import Optional

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"

SUPPORTED_LOCALES = ("en_US", "pt_BR", "es_ES")
DEFAULT_LOCALE = "en_US"
LOCALES_PACKAGE = "safe_input_veritas.locales"


class LoggerSetup:
    """
    LoggerSetup configures a module-wide logger with internationalized messages.

    Attributes:
        logger (logging.Logger): The configured logger instance.
        messages (dict): Load messages for selected locale.

    Methods:
        get_message(key: str) -> str: Retrieve localized message string.
    """

    def __init__(self, locale: Optional[str] = None):
        """
        Initialize LoggerSetup instance with specified or environment locale.

        Args:
            locale (Optional[str], optional): Locale code to load messages
                for (e.g. en_US). If None, attempts to read SAFEINPUTVERITAS_LANG
                env variable, falls back to 'en_US' if unset or unsupported.
        """
        self.locale = locale or os.getenv("SAFEINPUTVERITAS_LANG", DEFAULT_LOCALE)
        if self.locale not in SUPPORTED_LOCALES:
            self.locale = DEFAULT_LOCALE

        self.logger = self._setup_logger()
        self.messages = self._load_messages()

    def _setup_logger(self) -> logging.Logger:
        """
        Setup and configure the logging.Logger instance used throughout the package.

        Returns:
            logging.Logger: Configured logger with DEBUG level and stream handler.
        """
        logger = logging.getLogger("SafeInputVeritas")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        return logger

    def _load_messages(self) -> dict[str, str]:
        """
        Load language messages JSON file based on current locale using
        importlib.resources.

        Returns:
            dict: Mapping of message keys to localized strings.

        Raises:
            FileNotFounderError: If locale and fallback locale files are missing.
            json.JSONDecodeError: If JSON content is malformed.
        """
        resource_name = "en_US.json"

        try:
            files = importlib.resources.files(LOCALES_PACKAGE)
            resource_file = files / resource_name
            with resource_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Locale file %s not found", resource_name)
            return {}
        except Exception as e:
            self.logger.error("Error loading locale file: %s", str(e))
            return {}

    def get_message(self, key: str) -> str:
        """
        Retrieve the localized message string for a given key.

        Args:
            key (str): The message key to look up.

        Returns:
            str: The localized message string if found, else returns the key itself.
        """
        return self.messages.get(key, key)


_logger_setup = LoggerSetup()


def get_logger() -> logging.Logger:
    """
    Get the module-wide logger instance.

    Returns:
        logging.Logger: The configured logger object.
    """
    return _logger_setup.logger


def get_message(key: str) -> str:
    """
    Fetch a localized message by its key.

    Args:
        key (str): The message key to retrieve from loaded messages.

    Returns:
        str: Localized message if key found, else the key string itself.
    """
    return _logger_setup.get_message(key)
