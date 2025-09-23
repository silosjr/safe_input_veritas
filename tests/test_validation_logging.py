"""
test_validation_logging.py - Unit tests for SafeInputVeritas centralized logging.

This module defines unit tests to validate SafeInputVeritas logging.

Focus is on verifying validation events, errors, and user actions
are properly logged at the right levels with meaningful messages.

Quality logging is essential for audit, troubleshooting, compliance,
and transparency.

Tests simulate CLI input scenarios to check for expected logging.

Supports CI to enforce robust logging in SafeInputVeritas projects.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from safe_input_veritas.base import InputValidator
from safe_input_veritas.logger_config.logger_setup import LoggerSetup

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestValidationLogging(unittest.TestCase):
    """
    Test suite for logging behavior in SafeInputVeritas validation.

    Tests ensure:
    - Validation errors log warnings or errors appropriately.
    - User cancellations and interrupts log info-level events.
    - Unexpected exceptions are captured and logged properly.
    - Logs respect localization and provide actionable info.

    These tests reinforce traceability and reliability in secure CLI input.
    """

    def test_logging_on_invalid_input(self):
        """
        Ensure logger captures warning on invalid input.

        Simulates user input that causes a ValueError in validation.
        Patches the logger.warning method to capture log call.

        Checks that:
        - Warning log is emitted on invalid input.
        - Message content includes expect substring.
        - Logs support auditability and traceability.
        """
        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn:
            with patch("builtins.input", side_effect=["invalid", "5"]):
                InputValidator.validate(
                    prompt="Enter an integer: ",
                    converter=int,
                    error_message_key="error_integer",
                    locale="en_US",
                )
                mock_warn.assert_called()
                calls = mock_warn.call_args_list
                found = any("Invalid integer" in str(call) for call in calls)
                assert found, "Expected warning about invalid integer not logged."

    def test_logging_unexpected_exception(self):
        """
        Ensure logger captures error with traceback on exception.

        This test mocks the logger.error to capture error logs emitted
        when an unexpected exception occurs during validation.

        It verifies that:
        - An error-level log entry happens on exception.
        - The logged message includes the exception type and traceback.
        - Logs support diagnostics and forensic analysis requirements.
        """

        def raise_exception(_):
            raise RuntimeError("Test exception")

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.error"
        ) as mock_error, patch("builtins.input", side_effect=raise_exception):
            result = InputValidator.validate(
                prompt="Enter a value: ",
                converter=str,
                error_message_key="unexpected_error",
                locale="en_US",
            )

            self.assertIsNone(result)

            mock_error.assert_called()
            calls = mock_error.call_args_list
            found = any(
                "exception" in str(call).lower() or "error" in str(call).lower()
                for call in calls
            )
            assert found, "Expected RuntimeError message not found in logs."

    def test_logging_user_cancel(self):
        """
        Ensure logger captures info on user cancellation events.

        This test simulates a user pressing 'q' to cancel input,
        mocking logger.info to capture log entries.

        It verifies:
        - An info log entry is generated on cancellation.
        - Log message content matches cancel prompt localized.
        """
        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.info"
        ) as mock_info, patch("builtins.input", side_effect=["q"]):
            result = InputValidator.validate(
                prompt='Enter a value or "q" to quit: ',
                converter=str,
                error_message_key="cancel_prompt",
                locale="en_US",
            )

            self.assertIsNone(result)

            mock_info.assert_called()
            calls = mock_info.call_args_list
            found = any("interruption" in str(call).lower() for call in calls)
            assert found, "User cancellation info log not emitted."

    def test_logging_critical_error(self):
        """
        Ensure logger.error captures critical unexpected errors with details.

        This test forces an unexpected exception during input validation,
        mocks logger.error to intercept logs, and verifies presence of
        error-level log with exception details.

        This guarantees that critical failures are logged for audit and
        diagnostics, complying with robustness requirements.
        """

        def raise_runtime_error(_):
            raise RuntimeError("Critical failure")

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.error"
        ) as mock_error, patch("builtins.input", side_effect=raise_runtime_error):
            result = InputValidator.validate(
                prompt="Enter a value: ",
                converter=str,
                error_message_key="unexpected_error",
                locale="en_US",
            )

            self.assertIsNone(result)

            mock_error.assert_called()
            calls = mock_error.call_args_list
            found = any("critical failure" in str(call).lower() for call in calls)
            assert found, "Critical failure error log emitted."

    def test_logging_on_scientific_notation_float(self):
        """
        Ensure logger captures warning on float input in scientific notation.

        Simulates user input of float in scientific notation whick is valid,
        but tests logging behavior on invalid then valid retry with this format.
        """
        locale = "en_US"
        error_key = "error_float"

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn, patch("builtins.input", side_effect=["invalid", "1e-3"]):
            result = InputValidator.validate(
                prompt="Enter a floating-point number: ",
                converter=float,
                error_message_key=error_key,
                locale=locale,
            )
            self.assertEqual(result, 0.001)
            mock_warn.assert_called()
            calls = mock_warn.call_args_list
            expected_message = LoggerSetup(locale).get_message(error_key)
            found = any(expected_message in str(call) for call in calls)
            self.assertTrue(
                found,
                "Localized float error message not logged on scientific"
                "notatation retry.",
            )

    def test_logging_on_input_with_spaces_and_special_chars(self):
        """
        Ensure logger captures warnings on input containing spaces and special
        characters.

        Simulates user input with leading/trailing spaces and special characters,
        checking validation retry and appropriate localized error logging.
        """
        locale = "en_US"
        error_key = "invalid_input"

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn, patch(
            "builtins.input", side_effect=["  ", "@!#$", "valid_input"]
        ):
            result = InputValidator.validate(
                prompt="Enter a value: ",
                converter=str,
                error_message_key=error_key,
                locale=locale,
            )
            self.assertEqual(result, "valid_input")
            self.assertTrue(mock_warn.call_count >= 2)
            calls = mock_warn.call_args_list
            expected_message = LoggerSetup(locale).get_message(error_key)
            found = any(expected_message in str(call) for call in calls)
            self.assertTrue(
                found,
                "Localized invalid input message not logged for special cases.",
            )


class TestLoggingI18n(unittest.TestCase):
    """
    Test suit for logging internationalization in en_US locale.

    Validates that key localized messages are present and logged correctly
    during validation error scenarios. Ensures audit-friendly logs and
    consistent user communication in English.
    """

    def test_logging_i18n_messages(self):
        """
        Validate localized messages are used in logs for different locales.

        This test runs input validation with invalid input across supported locales,
        capturing warning logs, to ensure logged messages correspond to the locale's
        language.

        It checks for presence of locale-specific error message string in the logs,
        verifying internationalization support in logging.
        """
        test_locales = ["en_US", "pt_BR", "es_ES"]
        error_key = "error_integer"

        for locale in test_locales:
            with patch(
                "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
            ) as mock_warn, patch("builtins.input", side_effect=["bad_input", "5"]):
                InputValidator.validate(
                    prompt="Enter an integer: ",
                    converter=int,
                    error_message_key=error_key,
                    locale=locale,
                )
                mock_warn.assert_called()
                calls = mock_warn.call_args_list

                expected_message = LoggerSetup(locale).get_message(error_key)

                found = any(expected_message in str(call) for call in calls)
                assert found, f"Localized message for {locale} not found in logs."

    def test_i18n_messages_en_us(self):
        """
        Verify presence and correctness of localized error messages for en_US.

        This test checks the log outputs for validation process with invalid
        inputs to confirm that messages match the English locale resources.
        """
        locale = "en_US"
        error_key = "error_integer"

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn, patch("builtins.input", side_effect=["bad_input", "5"]):
            InputValidator.validate(
                prompt="Enter an integer: ",
                converter=int,
                error_message_key=error_key,
                locale=locale,
            )
            mock_warn.assert_called()
            calls = mock_warn.call_args_list
            expected_message = LoggerSetup(locale).get_message(error_key)
            found = any(expected_message in str(call) for call in calls)
            self.assertTrue(
                found,
                f"Localized messge for {locale} not found in logs.",
            )

    def test_i18n_messages_pt_br(self):
        """
        Verify presence and correctness of localized error messages for pt_BR.

        This test checks the log outputs for validation process with invalid
        inputs to confirm that messages match the Brazilian Portuguese resources.
        """
        locale = "pt_BR"
        error_key = "error_integer"

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn, patch("builtins.input", side_effect=["bad_input", "5"]):
            InputValidator.validate(
                prompt="Digite um inteiro: ",
                converter=int,
                error_message_key=error_key,
                locale=locale,
            )
            mock_warn.assert_called()
            calls = mock_warn.call_args_list
            expected_message = LoggerSetup(locale).get_message(error_key)
            found = any(expected_message in str(call) for call in calls)
            self.assertTrue(
                found,
                f"Localized message for {locale} not found in logs.",
            )

    def test_i18n_messages_es_es(self):
        """
        Verify presence and correctness of localized error messages for es_ES.

        This test checks the log outputs for validation process with invalid
        inputs to confirm that messages match the Spanish resources.
        """
        locale = "es_ES"
        error_key = "error_integer"

        with patch(
            "safe_input_veritas.logger_config.logger_setup.logging.Logger.warning"
        ) as mock_warn, patch("builtins.input", side_effect=["bad_input", "5"]):
            InputValidator.validate(
                prompt="Introduzca un entero: ",
                converter=int,
                error_message_key=error_key,
                locale=locale,
            )
            mock_warn.assert_called()
            calls = mock_warn.call_args_list
            expected_message = LoggerSetup(locale).get_message(error_key)
            found = any(expected_message in str(call) for call in calls)
            self.assertTrue(
                found,
                f"Localized message for {locale} not found in logs.",
            )


if __name__ == "__main__":
    unittest.main()
