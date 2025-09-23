"""
integer - Module for validating integer user input with internationalized logging.

This module provides a specialized IntegerValidator class which extends the
generic InputValidator base class to specifically handle integer inputs from
users in CLI applications.

It integrates with SafeInputVeritas centralized logging and internationalization
system, ensuring all user input validation follows consistent messaging,
error handling, and logging practices.

The IntegerValidator class provides a clear interface for integer input,
facilitating reuse and extensibility across different parts of the application.
"""

from __future__ import annotations

from typing import Optional

from safe_input_veritas.base import (
    InputValidator,
)
from safe_input_veritas.logger_config.logger_setup import (
    get_message,
)

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"


class IntegerValidator(InputValidator):
    """
    Validator class for integer inputs, extending the base InputValidator.

    This class encapsulates all logic and error messaging necessary to solicit,
    validate, and convert integer user input via CLI, integrating with the
    centralized logger and internationalized messages.

    Extending the base class allows easy customization and consistent handling
    of integers across the application.

    Attributes:
        None

    Methods:
        validate_integer(
        prompt: str = '',
        locale: Optional[str] = None
        ) -> Optional[int]:
            Prompts the user for integer input, performs validation and conversion
            logs validation steps, handles user cancellation and interruptions,
            and returns the valid integer or None if input was canceled.
    """

    @staticmethod
    def validate_integer(
        prompt: str = "",
        locale: Optional[str] = None,
    ) -> Optional[int]:
        """
        Prompt the user for an integer input, validating and handling errors.

        The function uses the base generic InputValidator's validate method,
        providing an integer casting function and localized error message.
        It repeats input requests until valid input or cancellation.

        Args:
            prompt (str, optional): The prompt shown to the user. If empty or
                not provided, a default localized prompt message is used.
            locale (Optional[str]): Optional locale code (e.g. 'pt_BR') for
                message localization.

        Returns:
            Optional[int]: The validated integer if successful; None if the user
                cancels input or interrupts the process.
        """
        error_message_key = "error_integer"
        if not prompt:
            prompt = get_message("input_prompt")

        return InputValidator.validate(prompt, int, error_message_key, locale=locale)
