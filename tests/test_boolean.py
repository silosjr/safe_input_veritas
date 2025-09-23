"""
test_boolean.py - Unit tests for BooleanValidator

This module provides a comprehensive suite of unit tests for the
BooleanValidator class, a specialized subclass of InputValidator designed
to securely validate and convert boolean user inputs in CLI environments.

The test suite encompasses:
- Correct parsing and conversion of boolean inputs.
- Handling of invalid boolean entries with retry and localized error prompts.
- Proper detection of user cancellations via 'q' and KeyboardInterrupt.
- Verification of logging and internationalization mechanisms.
- Integration and compliance with the generic InputValidator base class.

Tests utilize unittest and mocking frameworks to simulate diverse input
scenarios without interactive user involvement, fulfilling SafeInputVeritas
mission-critical input validation standards.

All tests adhere to best practices for clarity, maintainability, and serve
as executable documentation for boolean input validation logic.

Usage:
    Run standalone or with any unittest-compatible test runner.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from safe_input_veritas.boolean import BooleanValidator

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestBooleanValidator(unittest.TestCase):
    """
    Unit test suite for BooleanValidator.

    This class verifies the BooleanValidator's functionality, including:
    - Successful boolean input recognition and conversion.
    - Handling invalid inputs and enforcing retry with proper messaging.
    - User cancellation detection and correct return values.
    - Localization and logging compliance.
    - Adherence to InputValidator interface contracts.

    It employs patching to automate input provision and isolate BooleanValidator
    behavior for repeatable and accurate testing.
    """

    @patch("builtins.input", side_effect=["y"])
    def test_validate_successful_boolean(self, mock_input):
        """
        Test successful validation and conversion of a valid boolean input.

        Simulates user entering 'y' (case-insensitive) and verifies that
        BooleanValidator correctly converts it to True.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["maybe", "n"])
    def test_retry_on_invalid_boolean_then_valid(self, mock_input):
        """
        Test retry mechanism when user enters invalid boolean input, then valid.

        Simulates 'maybe' leading to ValueError and reprompt, followed by 'n'
        successfully converted to False.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["q"])
    def test_user_cancel(self, mock_input):
        """
        Test input cancellation by the user entering 'q'.

        Verifies that the validate_boolean method returns None to indicate
        graceful cancellation.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_input):
        """
        Test handling of user interruption by KeyboardInterrupt (Ctrl+C).

        Verifies validate_boolean returns None and exits gracefully on interruption.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=Exception("Unexpected error"))
    def test_unexpected_exception(self, mock_input):
        """
        Test handling of unexpected exceptions during boolean input solicitation.

        Ensures validate_boolean catches unexpected exceptions and returns None.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["   ", "y"])
    def test_empty_input_then_valid(self, mock_input):
        """
        Test behavior when user inputs empty string first then valid boolean.

        Verifies that empty input triggers retry and 'y' converts successfully.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean value (y/n): ", locale="en_US"
        )
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["n"])
    def test_empty_prompt_uses_default_prompt(self, mock_input):
        """
        Test that supplying  an empty prompt causes use of the default localized prompt.

        Ensures input 'n' is accepted using default prompt in validate_boolean.
        """
        result = BooleanValidator.validate_boolean(prompt="", locale="en_US")
        self.assertFalse(result)

    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    @patch("builtins.input", side_effect=["token987", "y"])
    def test_boolean_logs_no_sensitive_data(self, mock_input, mock_warn):
        """
        Test BooleanValidator does not expose sensitive data in logs.

        Simulates sensitive input and checks logged warnings for
        absence of sensitive substrings.

        Ensures retry works without exposing secrets.
        """
        sensitive_keywords = ["password", "secret", "token"]

        BooleanValidator.validate_boolean(prompt="Enter a boolean: ", locale="en_US")

        logged_messages = [call.args[0] for call in mock_warn.call_args_list]
        for message in logged_messages:
            for sensitive_word in sensitive_keywords:
                assert sensitive_word not in message.lower()
                f'Sensitive "{sensitive_word}" found in logs.'

    @patch("builtins.input", side_effect=["bad"] * 10 + ["y"])
    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    def test_boolean_long_retry_sequence(self, mock_warn, mock_input):
        """
        Test BooleanValidator stability with long invalid input sequences.

        Simulates 10 invalid inputs triggering warnings then a valid boolean.

        Verifies stable retry and proper final conversion.
        """
        result = BooleanValidator.validate_boolean(
            prompt="Enter a boolean: ", locale="en_US"
        )
        self.assertTrue(result)
        self.assertGreaterEqual(mock_warn.call_count, 10)


if __name__ == "__main__":
    unittest.main()
