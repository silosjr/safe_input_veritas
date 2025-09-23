"""
test_cli_utils.py - Test suite for cli_utils module of SafeInputVeritas.

This module contains unit tests for the command-line interface utility
functions provided by SafeInputVeritas. It ensures that CLI interaction
helpers behave correctly with respect to user prompts, message printing,
and logging, including support for internationalized messages.

Test coverage includes verifying proper invocation of input pauses,
informational message display, error message reporting, and correct
functional behavior, correct logging levels, and proper handling of
localized message retrieval.

All tests are implemented using unittest.mock for isolation and pytest
for execution and assertions, adhering to corporate code standards and
consistent documentation practices.
"""

from __future__ import annotations

from unittest import mock

from safe_input_veritas.cli_utils import (
    pause_prompt,
    print_error,
    print_info,
)

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestCliUtils:
    """
    Unit tests for SafeInputVeritas CLI utility functions.

    This class groups tests validating the cli_utils module functions that facilitate
    command-line user interactions. Focus areas include:
    - Confirming user prompt pauses block execution as expected while logging pause
      events.
    - Verifying informational messages are fetched from localization sources, logged
      at INFO level, and printed to the console.
    - Ensuring error messages are properly retrieved, logged at ERROR level, and
      output correctly to the console.

    The test methods employ mocks to isolate side effects such as input, print, and
    logging, thereby verifying the behavior of the cli_utils functions in predictable
    and controlled scenarios.
    """

    @mock.patch("builtins.input", return_value="")
    @mock.patch("safe_input_veritas.cli_utils.logger.info")
    def test_pause_prompt_logs_and_waits(self, mock_logger_info, mock_input):
        """
        Test that pause_prompt logs the pause and waits for user input.

        It should call input once and log the pause event at info level.
        """
        pause_prompt()
        mock_logger_info.assert_called_once_with(
            "Pausing execution, waiting for user to continue."
        )
        mock_input.assert_called_once()

    @mock.patch("builtins.print")
    @mock.patch("safe_input_veritas.cli_utils.logger.info")
    @mock.patch("safe_input_veritas.cli_utils.get_message", return_value="Test info")
    def test_print_info_prints_and_logs(
        self, mock_get_msg, mock_logger_info, mock_print
    ):
        """
        Test that print_info fetches message, logs it as info, and prints to console.
        """
        print_info("some_key")
        mock_get_msg.assert_called_once_with("some_key")
        mock_logger_info.assert_called_once_with("INFO: %s", "Test info")
        mock_print.assert_called_once_with("Test info")

    @mock.patch("builtins.print")
    @mock.patch("safe_input_veritas.cli_utils.logger.error")
    @mock.patch("safe_input_veritas.cli_utils.get_message", return_value="Test error")
    def test_print_error_prints_and_logs(
        self, mock_get_msg, mock_logger_error, mock_print
    ):
        """
        Test that print_error fetches message, logs it as error, and prints to console.

        It should call get_message with the provided key, log the message at ERROR
        level, and print the message to console.
        """
        print_error("error_key")
        mock_get_msg.assert_called_once_with("error_key")
        mock_logger_error.assert_called_once_with("ERROR: %s", "Test error")
        mock_print.assert_called_once_with("Test error")


if __name__ == "__main__":
    import sys

    import pytest

    exit_code = pytest.main([__file__, "-v", "--tb=short", "--no-header"])
    sys.exit(exit_code)
