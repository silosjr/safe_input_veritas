"""
test_base.py - Core module for generic and secure CLI user input validation.

This module provides the InputValidator class, which offers a generic mechanism
to solicit, validate, and safely convert CLI user input in Python.

Main features:
- Generic validation using a user-provided conversion callable.
- Handles invalid input, user cancellation (Ctrl+C, 'q'), and unexpected errors.
- Supports localization of messages (i18n).
- Incorporates structured logging for traceability.
- Implements an object-oriented design allowing subclassing and reusability.

All methods return None on user cancellation or error to ensure predictable
behavior in dependent applications.
"""

from __future__ import annotations

import unittest
from typing import Any, cast
from unittest.mock import patch

from safe_input_veritas.base import InputValidator

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class CustomError(ValueError):
    """
    Custom error that inherits from ValueError but is not caught by the first except.
    """

    pass


class TestInputValidator(unittest.TestCase):
    """
    Unit test suite for the InputValidator class.

    Tests cover normal operation, input errors, user cancellations, and
    exception handling to verify input validation robustness.

    This test suite employs mocking to simulate user inputs and captures output
    to verfify correct messages and logging behavior. It ensures that the
    InputValidator correctly converts valid inputs, properly handles invalid
    conversions by prompting retries, processes user cancellation via 'q' or
    KeyboardInterrupt without exceptions, and logs errors appropriately.
    """

    def setUp(self):
        """
        Setup for each test case if needed
        """
        pass

    @patch("builtins.input", side_effect=["42"])
    def test_validate_success(self, mock_input):
        """
        Test successful validation and conversion of user input.

        Simulates entering a valid integer string '42' and asserts that
        the InputValidator correctly converts and returns the integer 42.
        """
        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=int,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 42)

    @patch("builtins.input", side_effect=["q"])
    def test_validate_user_cancel(self, mock_input):
        """
        Test the validation flow when the user cancels input by entering 'q'.

        Simulates a user entering 'q' to cancel the input. Asserts that the
        validate method returns None and no exception is raised, representing
        a graceful cancellation.
        """
        result = InputValidator.validate(
            prompt="Enter a value: ",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["invalid", "10"])
    def test_validate_retry_on_value_error(self, mock_input):
        """
        Test repeated input attempts after a ValueError caused by invalid input.

        Simulates a user first entering an invalid string 'invalid' that triggers
        ValueError, followed by a valid input '10'. Confirms that the validator
        displays the error message and finally returns the correct converted value.
        """
        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=int,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 10)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_validate_user_keyboard_interrupt(self, mock_input):
        """
        Test handling of user cancellation via KeyboardInterrupt (Ctrl+C).

        Simulates raising KeyboardInterrupt during input solicitation. Verifies
        that the validate method catches the exception, logs appropriately, and
        returns None to signify graceful cancellation.
        """
        result = InputValidator.validate(
            prompt="Enter any value: ",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=Exception("Unexpected error"))
    def test_validate_unexpected_exception(self, mock_input):
        """
        Test handling of unexpected exception raised during input solicitation.

        Simulates a generic exception being raised during input call. Verifies that
        the validate function catches the exception, properly logs and prints the
        error message, and returns None to maintain predictable flow.
        """
        result = InputValidator.validate(
            prompt="Enter any value: ",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["   ", "5"])
    def test_validate_empty_input_then_valid(self, mock_input):
        """
        Test handling empty or whitespace-only input by retrieving until valid input.

        Simulates user first entering only spaces, which should cause validation
        to fail and prompt retry, then entering valid input '5'. Asserts that the
        method eventually returns the correctly converted integer value.
        """
        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=int,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 5)

    @patch("builtins.input", side_effect=["10"])
    def test_validate_with_none_converter(self, mock_input):
        """
        Test that validate method raises ValueError when converter is None.

        This test simulates valid input '10' but a None converter argument,
        expecting the method to raise ValueError indicating invalid converter.
        """
        with self.assertRaises(ValueError):
            InputValidator.validate(
                prompt="Enter a value: ",
                converter=None,
                error_message_key="invalid_input",
                locale="en_US",
            )
            mock_input.assert_called_once_with("Enter a value: ")

    @patch("builtins.input", side_effect=["ignored_input"])
    def test_validate_with_none_converter_raises(self, mock_input):
        """
        Test that validate raises ValueError if converter is None.
        """
        with self.assertRaises(ValueError) as context:
            InputValidator.validate(
                prompt="Enter a value: ",
                converter=None,
                error_message_key="invalid_input",
                locale="en_US",
            )
        self.assertIn("Converter", str(context.exception))

    @patch("builtins.input", side_effect=["hello"])
    def test_validate_empty_prompt_uses_default(self, mock_input):
        """
        Test that an empty prompt triggers use of the default localized prompt
        message.

        Simulates user input 'hello' when an empty string is provided to prompt
        argument. Verifies that the method uses the default prompt from
        localization and returns the correct conversion result.
        """
        result = InputValidator.validate(
            prompt="",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertEqual(result, "hello")

    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    @patch("builtins.input", side_effect=["password123", "valid_input"])
    def test_validate_logs_do_not_expose_sensitive_data(self, mock_input, mock_warn):
        """
        Test that validate method logs do not contain sensitive data during
        input validation.

        This simulates sensitive input and checks that logs do not contain
        sensitive data.

        The method retries on invalid input without exposing sensitive
        information in logs.
        """
        sensitive_keywords = ["password", "secret", "token"]

        InputValidator.validate(
            prompt="Enter a value: ",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )

        logged_messages = [call.args[0] for call in mock_warn.call_args_list]
        for message in logged_messages:
            for sensitive_word in sensitive_keywords:
                assert sensitive_word not in message.lower()
                f'Sensitive data "{sensitive_word}" found in logs.'

    @patch("builtins.input", side_effect=["bad"] * 10 + ["42"])
    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    def test_validate_long_retry_sequence(self, mock_warn, mock_input):
        """
        Test that validate properly retries and remains stable through a long series
        of invalid inputs before a valid one.

        Simulates user entering ten consecutive invalid strings, causing warnings each
        time, and finally a valid integer '42'.

        Ensures no exceptions are raised, the process stabilizes, and the final input
        is returned.

        It also verifies that a warning is logged at each invalid input.
        """
        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=int,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 42)
        self.assertGreaterEqual(mock_warn.call_count, 10)

    @patch("builtins.input", side_effect=["test", "valid_input"])
    def test_validate_with_unsupported_converter_type(self, mock_input):
        """
        Test handling of converter that raises TypeError instead of ValueError.

        Some converters may raises TypeError for certain invalid inputs,
        this test ensures proper handling of such cases.
        """

        def problematic_converter(value):
            if value == "test":
                raise TypeError("Unsupported type conversion.")
            return value

        result = InputValidator.validate(
            prompt="Enter a value: ",
            converter=problematic_converter,
            error_message_key="invalid_input",
            locale="en_US",
        )

        self.assertEqual(result, "valid_input")

    @patch("builtins.input", side_effect=["valid"])
    def test_validate_with_special_characters_in_prompt(self, mock_input):
        """
        Test validation with prompt containing special characters or very long text.

        Ensures the validator handles edge cases in prompt formatting.
        """
        special_prompt = "Enter value (ñ áéíóú 中文 emoji: 🚀): "
        result = InputValidator.validate(
            prompt=special_prompt,
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertEqual(result, "valid")

    @patch("builtins.input", side_effect=["123"])
    def test_validate_with_invalid_locale(self, mock_input):
        """
        Test validation with non-existent locale falls back gracefully.

        When an invalid locale is provided, the system should handle
        it gracefully and still function properly.
        """
        result = InputValidator.validate(
            prompt="Enter a number: ",
            converter=int,
            error_message_key="invalid_input",
            locale="xx_XX",
        )
        self.assertEqual(result, 123)

    @patch(
        "safe_input_veritas.cli_utils.get_message",
        side_effect=Exception("Message error"),
    )
    @patch("builtins.input", side_effect=["valid_value"])
    def test_validate_with_message_retrieval_error(self, mock_input, mock_get_message):
        """
        Test handling when get_message raises an exception.

        This test covers the case where message retrieval fails, tipically covering
        fallback message handling logic.
        """
        result = InputValidator.validate(
            prompt="Enter value: ",
            converter=str,
            error_message_key="some_key",
            locale="en_US",
        )
        self.assertEqual(result, "valid_value")

    @patch("safe_input_veritas.cli_utils.get_message", return_value="")
    @patch("builtins.input", side_effect=["test_value"])
    def test_validate_with_empty_retrieved_message(self, mock_input, mock_get_message):
        """
        Test handling when retrieved message is empty or None.

        Covers edge case where get_message returns empty string, forcing fallback to
        default behavior.
        """
        result = InputValidator.validate(
            prompt="",
            converter=str,
            error_message_key="empty_message_key",
            locale="en_US",
        )
        self.assertEqual(result, "test_value")

    @patch("safe_input_veritas.logger_config.logger_setup.logging.Logger.warning")
    @patch("builtins.input", side_effect=["", "   ", "q"])
    def test_validate_with_multiple_empty_inputs_then_quit(
        self, mock_input, mock_print_error
    ):
        """
        Test handling of multiple consecutive empty inputs followed by quit.

        This covers edge case logic where multiple empty strings are entered before
        user decides to quit with 'q'.
        """
        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=int,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertIsNone(result)
        self.assertGreaterEqual(mock_print_error.call_count, 2)

    @patch("builtins.input", side_effect=["bad_input", "valid_input"])
    def test_validate_converter_raises_exception(self, mock_input):
        """
        Test that an exception from converter causes a warning and retry input
        instead of crashing.
        """

        def faulty_converter(val):
            if val == "bad_input":
                raise Exception("Conversion failed.")
            return val

        result = InputValidator.validate(
            prompt="Enter a value: ",
            converter=faulty_converter,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertEqual(result, "valid_input")

    @patch("builtins.input", side_effect=["bad_value", "42"])
    def test_validate_catches_valueerror_and_retries(self, mock_input):
        """
        Tests that a ValueError from the converter triggers logging
        print error message, and does not exit but retries input.
        """

        def raises_value_error(val):
            if val == "bad_value":
                raise ValueError("Invalid input")
            return int(val)

        result = InputValidator.validate(
            prompt="Enter a number: ",
            converter=raises_value_error,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 42)

    @patch("builtins.input", side_effect=RuntimeError("Unexpected error"))
    def test_validate_unexpected_exception_break_loop(self, mock_input):
        """
        Test that unexpected exception breaks the loop, logs an error and returns None.
        """
        result = InputValidator.validate(
            prompt="Enter a value: ",
            converter=str,
            error_message_key="invalid_input",
            locale="en_US",
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["bad_value", "42"])
    def test_validate_with_value_error_causes_warning(self, mock_input):
        """
        Test handling of ValueError raised by converter.

        This test triggers except ValueError block that logs warning, prints error,
        and retries input.
        """

        def converter_raises_value_error(val):
            if val == "bad_value":
                raise ValueError("Invalid converter")
            return int(val)

        result = InputValidator.validate(
            prompt="Enter an integer: ",
            converter=converter_raises_value_error,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 42)

    @patch("builtins.input", side_effect=["bad_value", "42"])
    def test_validate_outer_value_error_block(self, mock_input):
        """
        Test triggering outer except ValueError block once, then
        converter works to exit loop.
        """
        call_count = {"count": 0}

        def raise_value_error_conditional(val):
            if call_count["count"] == 0:
                call_count["count"] += 1
                raise ValueError("Forced Error")
            return int(val)

        result = InputValidator.validate(
            prompt="Enter integer: ",
            converter=raise_value_error_conditional,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 42)

    @patch("builtins.input", side_effect=["invalid", "123"])
    def test_validate_covers_value_error_block(self, mock_input):
        """
        Trigger ValueError in converter to cover except ValueError block.

        This block logs, prints error, then continues input loop.
        """

        def converter_raises_value_error(val):
            if val == "invalid":
                raise ValueError("Invalid input for conversion")
            return int(val)

        result = InputValidator.validate(
            prompt="Enter integer: ",
            converter=converter_raises_value_error,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertEqual(result, 123)

    def test_attempt_conversion_with_non_callable_converter(self):
        """
        Test _attempt_conversion directly with non-callable converter.
        """
        with self.assertRaises(ValueError):
            InputValidator._attempt_conversion("test_input", cast(Any, 123))

    @patch("builtins.input", side_effect=["test_value", "q"])
    def test_validate_exception_isinstance_valueerror(self, mock_input):
        """
        Test that outer Exception handler correctly handles a ValueError
        by simulating converter raising ValueError
        """

        def converter_that_raises_exception_as_valueerror(val):
            raise ValueError("Test forced ValueError")

        result = InputValidator.validate(
            prompt="Test: ",
            converter=converter_that_raises_exception_as_valueerror,
            error_message_key="error_integer",
            locale="en_US",
        )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["test_value", "q"])
    def test_validate_exception_outer_catch_isinstance_check(self, mock_input):
        """
        Test that outer except Exception catches non-standar exceptions and
        correctly identifies if they are instances of ValueError/TypeError.
        """

        def converter_raises_custom_error(val):
            if val == "test_value":
                raise CustomError("Forced error for coverage")
            return val

        with patch("builtins.input", side_effect=[CustomError("Forced error"), "q"]):
            result = InputValidator.validate(
                prompt="Test: ",
                converter=str,
                error_message_key="error_integer",
                locale="en_US",
            )
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["test_value", "q"])
    @patch("safe_input_veritas.base.InputValidator._attempt_conversion")
    def test_validate_exception_isinstance_in_outer_except(
        self,
        mock_attempt,
        mock_input,
    ):
        """
        Force _attempt_conversion to raise a ValueError that gets caught
        by outer except.
        """
        mock_attempt.side_effect = [ValueError("Test error"), None]

        result = InputValidator.validate(
            prompt="Test: ",
            converter=str,
            error_message_key="error_integer",
            locale="en_US",
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
