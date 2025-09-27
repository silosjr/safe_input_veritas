"""
test_base - Formal Verification and Validation for the InputValidator Component.

This module provides the complete test suite for the `InputValidator` class, which
serves as the foundational component for the SafeInputVeritas framework. The tests
herein are engineered to provide a formal proof of correctness for the component's
behavior under a comprehensive set of operational and failure scenarios.

The testing strategy is predicated on achieving a hermetic environment for the
Component Under Test (CUT). All external dependencies, notably the `LoggerSetup`
subsystem is isolated via mocking. This ensures that the tests are deterministic,
fast, and validate only the logic intrinsic to the `InputValidator` itself.

Each test case is designed to prove a specific logical path, boundary condition, or
exception handling mechanism, thereby ensuring 100% logical coverage and compliance
with mission-critical software standards.
"""

from __future__ import annotations

import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from safe_input_veritas.base import InputValidator

__author__ = 'Enock Silos'
__email__ = 'init.caucasian722@passfwd.com'
__status__ = 'Verification'


class TestInputValidator(unittest.TestCase):
    """
    A test case suite for the `InputValidator` class.

    This suite verifies the correctness of the `InputValidator`'s contract, including
    its state initialization, orchestration of the input/validation loop, delegation to
    conversion strategies, and handling of all user interaction paths such as valid
    input, invalid input, and cancellation signals.
    """

    @patch("safe_input_veritas.base.LoggerSetup", autospec=True)
    def setUp(self, mock_logger_setup_class: MagicMock) -> None:
        """
        Establishes a hermetic test environment before each test execution.

        This method is invoked by the test runner prior to running each test.
        Its primary responsibility is to configure the controlled environment
        for the Component Under Test (CUT). It achieves this by:
            1.  Instantiating a mock for the `LoggerSetup` dependency, which isolates
                the CUT from the filesystem and logging infrastructure.
            2.  Configuring the mock's return values for predictable behavior.
            3. Instantiating the `InputValidator` with the mocked dependencies.
        """
        self.mock_logger_setup_instance = mock_logger_setup_class.return_value
        self.mock_logger = MagicMock()
        self.mock_logger_setup_instance.logger = self.mock_logger
        self.mock_logger_setup_instance.get_message.return_value = ("Mocked message")

        self.validator = InputValidator(locale="en_US")
        self.validator.logger_setup = self.mock_logger_setup_instance
        self.validator.logger = self.mock_logger

    def test_constructor_initializes_dependencies(self) -> None:
        """
        Verifies that the constructor correctly initializes all dependencies.

        This test proves that upon instantiation, the `InputValidator` class correctly
        creates and configures its required `LoggerSetup` service, passing the
        specified locale. This confirms the correct establishment of the validation
        context for the instance's lifecycle.
        """
        with patch(
            "safe_input_veritas.base.LoggerSetup", autospec=True
            ) as mock_constructor:
            mock_instance = mock_constructor.return_value
            mock_instance.logger = MagicMock()

            InputValidator(locale="fr_FR")

            mock_constructor.assert_called_once_with(locale="fr_FR")

    def test_attempt_conversion_delegates_successfully(self) -> None:
        """
        Verifies that `attempt_conversion` correctly delegates to the converter.

        This test validates the primary success path of the static helper method.
        It proves that the method acts as a direct, unmediated bridge to the provided
        conversion callable, returning its result without alteration.
        """
        input_string = "123"
        converter = int

        result = InputValidator._attempt_conversion(input_string, converter)

        self.assertEqual(result, 123)

    def test_attempt_conversion_propagates_exceptions(self) -> None:
        """
        Verifies that `attempt_conversion` propagates exceptions from the converter.

        This test proves that the method does not suppress or alter exceptions raised
        by the conversion strategy. It ensures that contract violations (e.g.,
        `ValueError` for invalid input) are correctly propagated up the call stack to
        be handled by the orchestrating logic.
        """
        def failing_converter(_: str) -> Any:
            raise ValueError("Conversion failed")

        with self.assertRaises(ValueError):
            InputValidator._attempt_conversion("invalid", failing_converter)

    @patch("builtins.input", return_value="42")
    def test_validate_returns_converted_value_on_success(
        self,
        mock_input: MagicMock
    ) -> None:
        """
        Verifies the primary success path of the input orchestration loop.

        This test simulates a complete, successful interaction. It proves that the
        `validate` method correctly prompts the user, receives valid input, delegates
        conversion, logs successful outcome for auditability, and returns the correctly
        typed final value.
        """
        prompt_message = "Enter number: "
        converter_strategy = int
        error_key = "error_integer"

        result = self.validator.validate(
            prompt_message, converter_strategy, error_key
        )

        mock_input.assert_called_once_with(prompt_message)
        self.assertEqual(result, 42)
        self.mock_logger.debug.assert_called_once()
        self.assertIn(
            "successfully validated", self.mock_logger.debug.call_args[0][0]
            )

    @patch("builtins.input", return_value="q")
    def test_validate_returns_none_on_user_quit_input(
        self,
        mock_input: MagicMock
    ) -> None:
        """
        Verifies the graceful cancellation path when the user enters "q".

        This test simulates a user explicitly aborting the input process.
        It proves that the validator correctly identifies the cancellation signal
        ("q"), logs the event for informational purposes, and returns `None` as per
        its contract for a controlled exit.
        """
        prompt_message = "Enter value: "

        result = self.validator.validate(prompt_message, str, "any_key")

        self.assertIsNone(result)
        self.mock_logger_setup_instance.get_message.assert_called_with(
            "user_interrupted"
            )
        self.mock_logger.info.assert_called_once_with("Mocked message")

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_validate_returns_none_on_keyboard_interrupt(
        self,
        mock_input: MagicMock
    ) -> None:
        """
        Verifies the graceful cancellation path upon a `KeyboardInterrupt` signal.

        This test simulates a user aborting the input process via Ctrl+C. It proves
        that the validator's outermost exception handler correctly catches
        `KeyboardInterrupt`, logs the event, and returns `None`, ensuring application
        stability and adherence to its cancellation contract.
        """
        prompt_message = "Enter value: "

        result = self.validator.validate(prompt_message, str, "any_key")

        self.assertIsNone(result)
        self.mock_logger_setup_instance.get_message.assert_called_with(
            "user_interrupted"
        )
        self.mock_logger.info.assert_called_once_with("Mocked message")

    @patch("builtins.input", side_effect=["", "  ", "valid"])
    def test_validate_reprompts_on_empty_or_whitespace_input(
        self,
        mock_input: MagicMock,
    ) -> None:
        """
        Verifies that empty or whitespace-only input is rejected and re-prompted.

        This test proves the input sanitization logic. It simulates a user providing
        empty and whitespace-only inputs, confirming that the validator rejects them,
        logs a warning, and continues the orchestration loop until a non-empty input
        is received.
        """
        prompt_message = "Enter value: "

        result = self.validator.validate(prompt_message, str, "any_key")

        self.assertEqual(result, "valid")
        self.assertEqual(self.mock_logger.warning.call_count, 2)
        self.mock_logger_setup_instance.get_message.assert_any_call("invalid_input")

    @patch("builtins.input", side_effect=["invalid", "42"])
    def test_validate_reprompts_on_conversion_value_error(
        self,
        mock_input: MagicMock,
    ) -> None:
        """
        Verifies the recovery path after a conversion strategy raises ValueError.

        This test simulates the most common failure scenario: invalid user input.
        It proves that when the converter delegate raises a `ValueError`, the
        validator correctly catches it, logs a warning, and re-prompts the user,
        eventually succeeding with a subsequent valid input. This confirms the
        robustness of the retry loop.
        """
        def converter_with_failure(value: str) -> int:
            if value == "invalid":
                raise ValueError("Invalid integer")
            return int(value)

        error_key = "error_integer"

        result = self.validator.validate(
            "Enter int: ", converter_with_failure, error_key
            )

        self.assertEqual(result, 42)
        self.mock_logger_setup_instance.get_message.assert_any_call(error_key)
        self.mock_logger.warning.assert_called_once()
        self.assertIn("Conversion failed", self.mock_logger.warning.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
