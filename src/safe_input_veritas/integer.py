"""
integer - Provides a specialized validator for integer user inputs.

This module defines the IntegerValidator class, a concrete implementation that extends
the Input Validator base class. Its primary function is to streamline the acquisition
and validation of integer data from command-line interfaces.

By encapsulating the integer-specific conversion logic and error messaging, this class
offers a simplified, high-level interface, ensuring consistency and robustness in
accordance with the application's core validation framework.
"""

from __future__ import annotations

from typing import Optional

from safe_input_veritas.base import InputValidator

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"


class IntegerValidator(InputValidator):
    """
    A specialized validator for acquiring and converting integer inputs.

    This class inherits the stateful, locale-aware orchestration logic from
    InputValidator. It specializes the validation process by pre-configuring
    it for integer conversion, thus abstracting the implementation details from
    the caller.

    An instanceof this class should be created for a specific validation context,
    potentially with a designated locale, which will govern all user-facing messages.
    """

    def get_integer(self, prompt: str = "") -> Optional[int]:
        """
        Orchestrates the prompting, validating, and converting of an integer.

        This method leverages the core validation loop of the parent class.
        It provides the necessary components for integer validation, specifically the
        `int` conversion function and the corresponding error message key. The method
        will persistently prompt the user until a valid integer is entered or the
        operation is explicitly canceled.

        Args:
            prompt (str, optional): The message displayed to the user. If omitted,
                a default message from the framework is utilized.

        Returns:
            Optional[int]: The validated integer value upon successful conversion.
                Returns `None` if the user cancels the operation (e.g., via `'q'`
                or `Ctrl+C`).
        """
        return super().validate(
            prompt=prompt, converter=int, error_message_key="error_integer"
        )
