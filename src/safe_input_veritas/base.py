"""
base.py - Provides foundational components for a robust input validation framework.

This module defines the `InputValidator` class, an architectural pattern designed
to orchestrate secure and reliable user input acquisition from command-line interfaces.
The design abstracts the complexities of I/O, error handling, and user cancellation
flows, delegating the specific validation logic to external, user-provided callables
(Strategy Pattern).

The architecture is engineered for mission-critical applications, incorporating
essential features such as structured, auditable logging and full internationalization
(i18n) support for all user-facing messages.
"""

from __future__ import annotations

from typing import Callable, Optional, TypeVar

from safe_input_veritas.logger_config.logger_setup import LoggerSetup

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Stable"

T = TypeVar("T")


class InputValidator:
    """
    A stateful orchestrator for user input interactions.

    Each instance of this class represents a self-contained validation context,
    encapsulating its own internationalization settings and logging components.
    It is designed to be instantiated with a specific locale, which then governs
    the language of all subsequent error messages and logs for that instance.
    """

    def __init__(self, locale: Optional[str] = None):
        """
        Constructs and configures an InputValidator instance.

        This constructor establishes the validation context for the object's entire
        lifecycle, primarily by initializing the logging and messaging subsystems
        according to the specified locale.

        Args:
            locale (Optional[str], optional): The locale identifier (e.g., "es_ES")
                that governs the language for all messages. If `None`, the locale is
                determined by the environment variable `SAFEINPUTVERITAS_LANG`, with
                a final fallback to the system default ("en_US").
        """
        self.logger_setup = LoggerSetup(locale)
        self.logger = self.logger_setup.logger

    @staticmethod
    def _attempt_conversion(value_str: str, converter: Callable[[str], T]) -> T:
        """
        Delegates the raw string conversion to the provided callable.

        This method acts a direct, unmediated bridge between the validation
        orchestrator and the specific conversion strategy. Its sole responsibility
        is to invoke the `converter` with the user's input.

        Args:
            value_str (str): The sanitized non-empty string provided by the user.
            converter (Callable[[str], T]): The validation and conversion function.

        Raises:
            ValueError: Propagates a `ValueError` if the `converter` function fails to
                process the input string.

        Returns:
            T: The converted value, now of the target type `T`.
        """
        return converter(value_str)

    def validate(
        self,
        prompt: str,
        converter: Callable[[str], T],
        error_message_key: str,
    ) -> Optional[T]:
        """
        Orchestrates the process of requesting, sanitizing, and validating user input.

        This method will loop until a valid input is provided or the user explicitly
        cancels the operation. It separates the orchestration logic from the specific
        validation rules, which are provided by the `converter`.

        Args:
            prompt (str): The message to display to the user when requesting input.
            converter (Callable[[str], T]): A callable that takes the user's string
                input and attempts to convert it to the target type `T`. It must raise
                a `ValueError` on conversion failure.
            error_message_key (str): The key to look up in the message files if the
                `converter` raises a `ValueError`.

        Returns:
            Optional[T]: An object of type `T` if validation is successful. `None` if
                the user cancels the operation (e.g., by typing `'q'` or pressing
                `Ctrl+C`).
        """
        effective_prompt = prompt or self.logger_setup.get_message("input_prompt")

        while True:
            try:
                user_input = input(effective_prompt).strip()

                if not user_input:
                    message = self.logger_setup.get_message("invalid_input")
                    self.logger.warning(message)
                    continue

                if user_input.lower() == "q":
                    message = self.logger_setup.get_message("user_interrupted")
                    self.logger.info(message)
                    return None

                validated_value = self._attempt_conversion(user_input, converter)

                converter_identifier_name = getattr(
                    converter, "__name__", type(converter).__name__
                )

                success_log_message = (
                    f"Input '{user_input}' successfully validated by "
                    f"'{converter_identifier_name}'. Result: {validated_value!r}"
                )
                self.logger.debug(success_log_message)

                return validated_value

            except ValueError:
                message = self.logger_setup.get_message(error_message_key)
                self.logger.warning(
                    "Conversion failed for input '%s': %s", user_input, message
                )
                continue

            except KeyboardInterrupt:
                message = self.logger_setup.get_message("user_interrupted")
                self.logger.info(message)
                return None
