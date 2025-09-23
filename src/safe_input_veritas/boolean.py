"""
boolean - Module for validating boolean user input with internationalized logging.

This module provides a specialized BooleanValidator class which extends the generic
InputValidator base class to specifically handle boolean inputs from
users in CLI applications.

It integrates with SafeInputVeritas centralized logging and internationalization
system, ensuring all user input validation follows consistent messaging,
error handling, and logging practices.

The BooleanValidator class provides a clear interface for boolean input, facilitating
reuse and extensibility across different parts of the application.
"""

from __future__ import annotations

from typing import Optional

from safe_input_veritas.base import InputValidator
from safe_input_veritas.logger_config.logger_setup import (
    get_message,
)

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"


class BooleanValidator(InputValidator):
    """
    Validator class for boolean inputs, extending the base InputValidator.

    This class encapsulates all logic and error messaging necessary to solicit,
    validate, and convert boolean user input via CLI, integrating with the
    centralized logger and internationalized messages.

    Extending the base class allows easy customization and consistent handling
    of booleans across the application.

    Attributes:
        None

    Methods:
        validate_boolean(
        prompt: str = '',
        locale: Optional[str] = None,
        ) -> Optional[bool]:
            Prompts the user for boolean input, performs validation and conversion,
            logs validation steps, handles user cancellation and interruptions,
            and returns the valid boolean or None if input was canceled.
    """

    @staticmethod
    def validate_boolean(
        prompt: str = "",
        locale: Optional[str] = None,
    ) -> Optional[bool]:
        """
        Prompt the user for a boolean input, validating and handling errors.

        Accepts user input in forms like 'y', 'n', 'yes', 'no' (case insensitive).

        Args:
            prompt (str, optional): The prompt shown to the user. If empty or
                not provided, a default localized prompt message is used.
            locale (Optional[str]): Optional locale code (e.g. 'en_US')
                for message localization.

        Returns:
            Optional[bool]: The validated boolean if successful; None if the user
                             cancels input or interrupts the process.
        """
        error_message_key = "error_boolean"
        if not prompt:
            prompt = get_message("input_prompt")

        def convert_to_bool(user_input: str) -> bool:
            normalized = user_input.strip().lower()
            if normalized in ("y", "yes"):
                return True
            elif normalized in ("n", "no"):
                return False
            else:
                raise ValueError("Invalid boolean input")

        return InputValidator.validate(
            prompt, convert_to_bool, error_message_key, locale=locale
        )
