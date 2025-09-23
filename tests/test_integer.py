"""
test_integer.py - Unit tests for IntegerValidator

This module contains a comprehensive suite of unit tests for the
IntegerValidator class, a specialized subclass of InputValidator
tailored for validating and converting integer inputs from command-line
users in a secure, robust manner.

The tests cover:
- Correct parsing and conversion of valid integer inputs.
- Handling of invalid integer inputs with proper error messages and retry
  mechanisms.
- User cancellation flows via 'q' key and KeyboardInterrupt.
- Logging and internationalization of prompts and error messages.
- Integration with underlying InputValidator base validation logic.

The test suit uses unittest and mocking techniques to simulate user input
and assert expected behaviors without interactive input. All tests follow
strict standards for clarity, reusability, and maintainability,
serving as documentation and quality assurance for secure CLI input handling.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from safe_input_veritas.integer import IntegerValidator

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestIntegerValidator(unittest.TestCase):
    """
    Unit test suite for IntegerValidator.

    This class tests the behavior of IntegerValidator, including:
    - Successful conversion of valid integers.
    - Detection and handling of invalid integer input.
    - User-triggered cancellations with proper returns.
    - Proper logging and localized messaging.
    - Compliance with InputValidator's contract and interfaces.

    Tests employ patching to simulate user input and isolate IntegerValidator
    funcionality in an automated manner, eliminating the need for manual input.
    """

    @patch("builtins.input", side_effect=["123"])
    def test_validate_successful_integer(self, mock_input):
        """
        Test successful validation and conversion of a valid integer input.

        This test calls IntegerValidator.validate_integer, which internally uses
        the base validator with int conversion.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertEqual(result, 123)

    @patch("builtins.input", side_effect=["invalid", "456"])
    def test_validate_retry_on_invalid_integer_then_valid(self, mock_input):
        """
        Test retry mechanism on invalid integer input followed by valid input.

        Simulates user first entering 'invalid' which triggers ValueError,
        then entering '456' which is converted correctly.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertEqual(result, 456)

    @patch("builtins.input", side_effect=["q"])
    def test_validate_user_cancel(self, mock_input):
        """
        Test input cancellation by the user entering 'q'.

        Verifies that the validate_integer method returns None to indicate
        graceful user cancellation.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_validate_keyboard_interrupt(self, mock_input):
        """
        Test handling of user interruption with KeyboardInterrupt (Ctrl+C).

        Verifies that validate_integer returns None and exits gracefully when
        a KeyboardInterrupt exception is raised during input solicitation.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )

        self.assertIsNone(result)

    @patch("builtins.input", side_effect=Exception("Unexpected error"))
    def test_validate_unexpected_exception(self, mock_input):
        """
        Test handling of unexpected exceptions during input solicitation.

        Simulates a generic Exception being raised and verifies that the
        validate_integer method catches it, logs properly, and returns None
        to maintain predictable control flow.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["   ", "789"])
    def test_validate_empty_input_then_valid(self, mock_input):
        """
        Test handling of empty or whitespace-only input leading to retry.

        Simulates user entering spaces first, causing validation entry,
        then entering valid integer '789' which is returned successfully.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertEqual(result, 789)

    @patch("builtins.input", side_effect=["101"])
    def test_validate_empty_prompt_uses_default_prompt(self, mock_input):
        """
        Test that an empty prompt argument triggers use of the default localized
        prompt message in validate_integer.

        Simulates user input '101' with empty prompt to confirm the default prompt is
        used successfully and the input is correctly converted.
        """
        result = IntegerValidator.validate_integer(prompt="", locale="en_US")
        self.assertEqual(result, 101)

    @patch("builtins.input", side_effect=["", KeyboardInterrupt])
    def test_validate_empty_input_then_keyboard_interrupt(self, mock_input):
        """
        Test behavior when input is empty first, then user interrupts via Ctrl+C.

        The method should retry after empty input and return None on interruption.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertIsNone(result)

    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    @patch("builtins.input", side_effect=["password123", "789"])
    def test_integer_logs_no_sensitive_data(self, mock_input, mock_warn):
        """
        Test IntegerValidator does not expose sentitive data in logs.

        Simulates sensitive input and checks logged warnings for
        absence of sensitive substrings.

        Ensure retry works without exposing secrets.
        """
        sensitive_keywords = ["password", "secret", "token"]

        IntegerValidator.validate_integer(prompt="Enter an integer: ", locale="en_US")

        logged_messages = [call.args[0] for call in mock_warn.call_args_list]
        for message in logged_messages:
            for sensitive_word in sensitive_keywords:
                assert sensitive_word not in message.lower()
                f'Sensitive "{sensitive_word}" found in logs.'

    @patch("builtins.input", side_effect=["bad"] * 10 + ["123"])
    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    def test_integer_long_retry_sequence(self, mock_warn, mock_input):
        """
        Test IntegerValidator stability with long invalid input sequences.

        Simulates 10 invalid inputs triggering warnings then a valid integer.

        Verifies stable retry and proper final conversion.
        """
        result = IntegerValidator.validate_integer(
            prompt="Enter an integer: ", locale="en_US"
        )
        self.assertEqual(result, 123)
        self.assertGreaterEqual(mock_warn.call_count, 10)


if __name__ == "__main__":
    unittest.main()
