"""
SafeInputVeritas - A robust user input validation framework.

This module provides the foundational InputValidator class, which offers a
generic, reusable mechanism to safely acquire and validate user input from
the command line inteface (CLI). It abstracts away repetitive I/O logic
and error handling, enabling strict and customizable validation via user-
provided conversion functions.

Features include:
- Generic validate method supporting any conversion callable that raises
  ValueError on invalid input.
- Graceful handling of user cancellation actions (Ctrl+C or 'q' key).
- Extensible design allowing subclassing for specific data types (int, float,
  bool) with standardized error messages and logic encapsulation.
- Design with the best practices for production-ready code including
  internationalization support (i18n), structured logging, and testability.
- Targeted for use in security-sensitive applications demanding zero-trust
  input handling and auditability.

All methods return None on user cancellation or unhandled exceptions to
guarantee a predictable flow in calling code. This module follows PEP-8
style guidelines and limits line length to 88 characters for readability.
"""

from __future__ import annotations

import re
from typing import Callable, Optional, TypeVar

from safe_input_veritas.logger_config.logger_setup import (
    LoggerSetup,
    get_logger,
)

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"

T = TypeVar("T")
logger = get_logger()


class InputValidator:
    """
    Base class to obtain and validate user input generically with internationalized
    message and logging support.

    This class provides a generic input validation engine for CLI applications
    by requesting user input, applying a conversion function, and
    handling exceptions gracefully, including cancellation via 'q' key or Ctrl+C.

    Support dynamics language selection via optional `locale` parameter,
    falling back to environment variable `SAFEINPUTVERITAS_LANG` or default
    'en_US'.

    Attributes:
        None

    Methods:
        validate(
        prompt: str,
        converter: Callable[[str], T]),
        error_message_key: str,
        locale: Optional[str] = None,
        ) -> Optional[T]:
            Solicits input, applies converter, retries on ValueError, and returns None
            if the user cancels input or on unexpected errors.

    Usage:
        Instantiate or subclass and call validate with appropriate parameters.
    """

    @staticmethod
    def _attempt_conversion(
        value_str: str, converter: Optional[Callable[[str], T]]
    ) -> T:
        """
        Attempt to convert input string to target type using provided converter.

        Args:
            value_str (str): Raw user input.
            converter (Optional[Callable[[str], T]]): Conversion Function.

        Raises:
            ValueError: For invalid conversions or empty string results.
            TypeError: If converter is not callable.

        Returns:
            T: Converted value.
        """
        if converter is None or not callable(converter):
            error_message = "Converter must be callable."
            logger.error(error_message)
            raise ValueError(error_message)

        converted = converter(value_str)

        if isinstance(converted, str):
            if not re.search(r"\w", converted):
                raise ValueError("Converted string invalid.")

        return converted

    @staticmethod
    def validate(
        prompt: str,
        converter: Optional[Callable[[str], T]],
        error_message_key: str,
        locale: Optional[str] = None,
    ) -> Optional[T]:
        """
        Prompt the user for input, apply safe conversion and flexible validation
        with support for localized messages and structured logging.

        Args:
            prompt (str): The message displayed to request user input.
            converter (Optional[[str], T]): Function converting input string to
                target type, raising ValueError on invalid input.
            error_message_key (str): Key to fetch localized error message shown
                when conversion fails.
            locale (Optional[str]): Locale code for internationalization, defaults
                if None.

        Returns:
            Optional[T]: Converted value if valid, None if user cancels input ('q' or
                Ctrl+C) or on unexpected errors.

        Raises:
            ValueError: In `converter` parameter is None.
            Exception: For unexpected errors during the input validation loop.
        """
        logger_setup = LoggerSetup(locale)

        if converter is None:
            error_message = logger_setup.get_message("converter_none_error")
            logger_setup.logger.error(error_message)
            raise ValueError(error_message)

        effective_prompt = prompt or logger_setup.get_message("input_prompt")

        while True:
            try:
                user_input = input(effective_prompt).strip()

                if not user_input:
                    logger_setup.logger.warning(
                        logger_setup.get_message("invalid_input")
                    )
                    continue

                if user_input == "q":
                    logger_setup.logger.info(
                        logger_setup.get_message("user_interrupted")
                    )
                    return None

                try:
                    value = InputValidator._attempt_conversion(user_input, converter)
                except Exception:
                    error_message = logger_setup.get_message(error_message_key)
                    logger_setup.logger.warning(error_message)
                    print(error_message)
                    continue

                return value

            except KeyboardInterrupt:
                logger_setup.logger.info(logger_setup.get_message("user_interrupted"))
                print()
                return None

            except Exception as e:
                if isinstance(e, (ValueError, TypeError)):
                    error_message = logger_setup.get_message(error_message_key)
                    logger_setup.logger.warning(error_message)
                    print(error_message)
                    continue

                error_message = logger_setup.get_message("unexpected_error").format(
                    details=e
                )
                logger_setup.logger.error(error_message)
                print(error_message)
                break

        return None
