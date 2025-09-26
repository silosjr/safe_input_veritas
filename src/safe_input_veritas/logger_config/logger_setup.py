"""
logger_setup - Centralized logging setup and internationalized messages.

This module provides the LoggerSetup class, which configures the application-wide
logging system for SafeInputVeritas and manages internationalized messages.

It provides a configurable logger suitable for CLI and production use. It also
manages message templates for validation events and errors, supporting multiple
locales.

Features:
- Standardized logging format with timestamps, levels and message context.
- Internationalized using importlib.resources for packaged locale files.
- Language selection via environment variable or passed during instantiation.
- Centralized message repository to avoid hardcoded strings in code.
- Designed for extensibility to support new languages and log handlers.

Usage:
Instantiate the LoggerSetup class to create a configured logger context:
>>> `logger_config = LoggerSetup(locale="pt_BR")`
>>> `logger = logger_config.logger`
>>> `message = logger_config.get_message("some_key")`
"""

from __future__ import annotations

import importlib.resources
import json
import logging
import os
from typing import Dict, Optional

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"

SUPPORTED_LOCALES = ("en_US", "pt_BR", "es_ES")
DEFAULT_LOCALE = "en_US"
LOCALES_PACKAGE = "safe_input_veritas.locales"


class ConfigurationError(Exception):
    """
    Custom exception for critical configuration failures.
    """


class LoggerSetup:
    """
    Configures a logger instance with internationalized message support.

    Each instance of this class represents a logging context for a specific locale,
    loading the appropriate messages and providing a configured logger object.

    Attributes:
        logger(logging.Logger): The configured logger instance.
        messages (Dict[str, str]): The loaded messages for the selected locale.
        locale (str): The effective locale used by the instance.
    """

    def __init__(self, locale: Optional[str] = None):
        """
        Initializes the LoggerSetup with a specific locale configuration.

        Args:
            locale (Optional[str]): The locale code (e.g., "pt_BR"). If `None`,
                it attempts to use the `SAFEINPUTVERITAS_LANG` environment variable,
                falling back to the default locale if necessary.
        """
        self.locale = locale or os.getenv("SAFEINPUTVERITAS_LANG", DEFAULT_LOCALE)

        if self.locale not in SUPPORTED_LOCALES:
            self.locale = DEFAULT_LOCALE

        self.logger = self._setup_logger()
        self.messages = self._load_messages()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up and configure the logging.Logger instance.

        Returns:
            logging.Logger: A configured logger with a DEBUG level and a standardized
                format via a stream handler.
        """
        logger = logging.getLogger(f"SafeInputVeritas.{self.locale}")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        return logger

    def _load_messages(self) -> Dict[str, str]:
        """
        Load language messages from a JSON file based on the instance's locale.

        Attempts to load the specific locale first. If that fails due to the file
        not being found or being malformed, it logs a warning and attempts to load
        the default fallback locale file as a safety measure.

        Returns:
            Dict[str, str]: A mapping of message keys to localized strings.

        Raises:
            ConfigurationError: If the fallback locale file is also missing or
                malformed, indicating a critical deployment error..
        """
        primary_resource = f"{self.locale}.json"
        fallback_resource = f"{DEFAULT_LOCALE}.json"
        package_files = importlib.resources.files(LOCALES_PACKAGE)

        try:
            resource_file = package_files / primary_resource
            with resource_file.open("r", encoding="utf-8") as f:
                self.logger.debug("Loaded locale messages from %s", primary_resource)
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(
                "Locale file '%s' not found. Attempt to fallback to '%s'.",
                primary_resource,
                fallback_resource,
            )

        try:
            resource_file = package_files / fallback_resource
            with resource_file.open("r", encoding="utf-8") as f:
                self.logger.info(
                    "Successfully loaded fallback locale: %s", fallback_resource
                )
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            log_message = (
                "CRITICAL: Fallback locale file '%s' is missing or corrupt."
                "The application cannot continue without messages."
            )
            self.logger.critical(log_message, fallback_resource)
            raise ConfigurationError(log_message % fallback_resource) from e

    def get_message(self, key: str) -> str:
        """
        Retrieve the localized message string for a given key.

        Args:
            key (str): The message key to look up.

        Returns:
            str: The localized message string if found; otherwise, returns the key
                itself enclosed in brackets as a fallback.
        """
        return self.messages.get(key, f"[{key}]")
