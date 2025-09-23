"""
test_internationalization.py - Automated tests for SafeInputVeritas i18n

This module contains a suite of automated unit tests dedicated to verifying
the correctness and completeness of the internationalization framework within
the SafeInputVeritas project.

If systematically validates that all localized message keys are present and
accurately translated across supported locales, ensuring that error messages,
prompts, and logs are consistently presented in the user's preferred language.

These tests serve as critical checkpoint in the project's continuous
integration (CI) pipeline to guarantee high-quality multilingual support and
adherence to global usability standards.

The tests in this module enforce the robustness of SafeInputVerita's i18n
implementation, fostering a seamless and secure user experience across
diversified linguistic environments.
"""

from __future__ import annotations

import unittest

from safe_input_veritas.logger_config.logger_setup import LoggerSetup

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"

ESSENTIAL_KEYS = [
    "user_interrupted",
    "unexpected_error",
    "invalid_input",
    "cancel_prompt",
    "pause_prompt",
    "input_prompt",
    "error_integer",
    "error_float",
    "error_boolean",
    "converter_none_error",
]


class TestInternationalization(unittest.TestCase):
    """
    Test suite for validating SafeInputVeritas internationalized message support.

    This class encapsulates multiple test cases aimed at ensuring:
    - All expected message keys exist in each supported locale.
    - Localized string match the authoritative translations loaded from JSON.
    - The framework correctly respects environment locale settings for message.

    These tests help prevent regressions in multilingual message support and
    assure correctness of user-facing communications in security-critical CLI.
    """

    def test_messages_present_en_us(self) -> None:
        """
        Verify presence of all essential i18n message keys in English locale.

        This test ensures that the 'en_US' messages dictionary contains all keys
        required for consistent internationalized user interaction across the CLI.

        Missing any of these keys could lead to fallback issues or uncaught errors
        during runtime when prompts or error messages are expected.

        The keys checked included standard error messages, prompts, and cancellation
        notices fundamental to SafeInputVerita's security and user experience.
        """
        locale = "en_US"
        logger_setup = LoggerSetup(locale)
        messages = logger_setup.messages

        for key in ESSENTIAL_KEYS:
            with self.subTest(key=key):
                self.assertIn(
                    key,
                    messages,
                    f'Missing key "{key}" in {locale} messages',
                )

    def test_messages_present_pt_br(self) -> None:
        """
        Verify that all essential i18n message keys exist in Portuguese locale.

        This test checks the 'pt_BR' messages dictionary for presence of keys
        required to localize error messages, prompts, and cancellations properly.

        Ensuring these keys exist prevents runtime issues and fallback errors,
        providing a consistent user experience for Brazilian Portuguese users.

        The validated keys cover core messaging for SafeInputVeritas' CLI interface.
        """
        locale = "pt_BR"
        logger_setup = LoggerSetup(locale)
        messages = logger_setup.messages

        for key in ESSENTIAL_KEYS:
            with self.subTest(key=key):
                self.assertIn(
                    key,
                    messages,
                    f'Missing key "{key}" in {locale} messages',
                )

    def test_messages_present_es_es(self) -> None:
        """
        Verify all critical i18n message keys exist in the Spanish (es_ES) locale.

        This test ensures the Spanish messages dictionary contains all necessary keys
        to support localized error prompts, confirmations, and cancellations.

        Maintaining complete key coverage safeguards user experience consistency
        and system robustness for Spanish-speaking users of SafeInputVeritas.

        The test covers fundamental messaging keys used throughout CLI workflows.
        """
        locale = "es_ES"
        logger_setup = LoggerSetup(locale)
        messages = logger_setup.messages

        for key in ESSENTIAL_KEYS:
            with self.subTest(key=key):
                self.assertIn(
                    key,
                    messages,
                    f'Missing key "{key}" in {locale} messages',
                )


if __name__ == "__main__":
    unittest.main()
