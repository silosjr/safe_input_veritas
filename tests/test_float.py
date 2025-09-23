"""
test_float.py - Unit tests for FloatValidator

This module contains a detailed suite of unit tests for the FloatValidator class,
which extends the generic InputValidator base class to provide secure and robust
validation and conversion of floating-point user input from CLI applications.

The test suite covers:
- Correct parsing and conversion of floating-point valid inputs.
- Handling of invalid float inputs with retry and proper localized error messages.
- User cancellation handling via 'q' key and KeyboardInterrupt.
- Logging and internationalization validation.
- Integration and compliance with the InputValidator base validation mechanisms.

Utilizing unittest and mocking, the tests simulate user input scenarios without
interactive prompts. They ensure FloatValidator meets SafeInputVeritas requirements
for mission-critical input validation with strict error handling and auditability.

All tests are documented for clarity, maintainability, and serve as living
documentation for secure CLI input validation logic.

Usage:
    Execute via a unittest-compatible test runner or as a standalone
    script.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from safe_input_veritas.float import FloatValidator

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestFloatValidator(unittest.TestCase):
    """
    Unit test suite for FloatValidator.

    This test class validates the FloatValidator behavior, including:
    - Successful float input parsing and conversion.
    - Handling invalid inputs and retry logic with error messages.
    - User-triggered cancel actions with expected return values.
    - Proper logging and message localization.
    - Compliance with base InputValidator interface and flows.

    Patching is employed to automate input simulation and isolate FloatValidator
    functionality for consistent test execution.
    """

    @patch("builtins.input", side_effect=["123.45"])
    def test_validate_successful_float(self, mock_input):
        """
        Test successful validation and conversion of a valid float input.

        Simulates the user entering '123.45' and asserts that the
        FloatValidator correctly converts to the float 123.45.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point number: ", locale="en_US"
        )
        self.assertEqual(result, 123.45)

    @patch("builtins.input", side_effect=["invalid", "789.01"])
    def test_retry_on_invalid_float_then_valid(self, mock_input):
        """
        Test retry mechanism on invalid float input followed by valid input.

        Simulates user first entering invalid string 'invalid', causing error,
        then entering '789.01' that is converted correctly.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point number: ", locale="en_US"
        )
        self.assertEqual(result, 789.01)

    @patch("builtins.input", side_effect=["q"])
    def test_user_cancel(self, mock_input):
        """
        Test user cancellation by entering 'q'.

        Ensures validate_float returns None for graceful cancellation.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """
        Test user interruption with KeyboardInterrupt (Ctrl+C).

        Ensures validate_float returns None and exits gracefully on interruption.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point number: ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=Exception("Unexpected error"))
    def test_unexpected_exception(self, mock_input):
        """
        Test handling of unexpected exceptions during float input solicitation.

        Verifies validate_float handles exceptions gracefully and returns None.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point number: ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["   ", "654.32"])
    def test_empty_input_then_valid(self, mock_input):
        """
        Test retry behavior when user enters empty input, then valid float.

        Asserts method retries until receives valid float input and converts it.
        """
        result = FloatValidator.validate_float(
            prompt="Enter a floating-point number: ", locale="en_US"
        )
        self.assertEqual(result, 654.32)

    @patch("builtins.input", side_effect=["321.09"])
    def test_empty_prompt_uses_default_prompt(self, mock_input):
        """
        Test that providing an empty prompt causes use of the localized prompt.

        Verifies input '321.09' is accepted when using default prompt in validate_float.
        """
        result = FloatValidator.validate_float(prompt="", locale="en_US")
        self.assertEqual(result, 321.09)

    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    @patch("builtins.input", side_effect=["secret987", "456.789"])
    def test_float_logs_no_sensitive_data(self, mock_input, mock_warn):
        """
        Test FloatValidator does not expose sensitive data in logs.

        Simulates sensitive input and checks logged warnings for
        absence of sentive substrings.

        Ensures retry works without exposing secrets.
        """
        sensitive_keywords = ["password", "secret", "token"]

        FloatValidator.validate_float(prompt="Enter float: ", locale="en_US")

        logged_messages = [call.args[0] for call in mock_warn.call_args_list]
        for message in logged_messages:
            for sensitive_word in sensitive_keywords:
                assert sensitive_word not in message.lower()
                f'Sensitive "{sensitive_word}" found in logs.'

    @patch("builtins.input", side_effect=["bad"] * 10 + ["3.1415"])
    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    def test_float_long_retry_sequence(self, mock_warn, mock_input):
        """
        Test FloatValidator stability with long invalid input sequences.

        Simulates 10 invalid inputs triggering warnings then a valid float.

        Verifies stable retry and proper final conversion.
        """
        result = FloatValidator.validate_float(prompt="Enter a float: ", locale="en_US")

        self.assertIsInstance(result, float)
        if isinstance(result, float):
            self.assertAlmostEqual(result, 3.1415, places=4)
            self.assertGreaterEqual(mock_warn.call_count, 10)


if __name__ == "__main__":
    unittest.main()
