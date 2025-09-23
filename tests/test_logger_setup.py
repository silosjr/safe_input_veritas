"""
test_logger_setup.py - Unit tests for LoggerSetup component.

This module provides a full test suite for the LoggerSetup class in the
SafeInputVeritas framework.

LoggerSetup initializes and configures application logging, including locale-based
message loading and setting up handlers.

Tests validate:
- Proper creation and addition of logging handlers when absent.
- Robust error handling when locale resource files are missing or inaccessible.
- Graceful recovery from unexpected exceptions during message loading.

These tests ensure reliability and fault tolerance of logging setup, critical for
auditability and traceability in security-sensitive applications.

All tests use mocks to isolate LoggerSetup behavior, ensuring deterministic,
reproducible outcomes.
"""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from safe_input_veritas.logger_config.logger_setup import LoggerSetup

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Verification"


class TestLoggerSetup(unittest.TestCase):
    """
    Unit test suite for rigorously verify behavior of LoggerSetup component
    within the SafeInputVeritas framework.

    The test focus on:
    - Proper handler creation when none exist on the logger.
    - Robustness against locale resource file absence (FileNotFoundError).
    - Resilience to generic exceptions during locale file loading.

    These tests ensure high reliability, fault tolerance, and compliance
    with corporate logging standards under exceptional conditions.
    """

    def test_creates_handler_if_none(self):
        """
        Verify LoggerSetup properly detects absence of logging handlers in a logger
        instance, and correctly adds a new StreamHandler as required to ensure log
        output is handled when none exist.
        """
        with patch("logging.getLogger") as m_get_logger:
            m_logger = Mock()
            m_logger.hasHandlers.return_value = False
            m_get_logger.return_value = m_logger

            _ = LoggerSetup("en_US")

            m_logger.addHandler.assert_called_once()

    def test_handles_file_not_found_error(self):
        """
        Validate that LoggerSetup gracefully handles the scenario where to locale
        resource file cannot be found, triggering a FileNotFoundError, and that the
        system falls back appropriately by using an empty messages dictionary without
        crashing.
        """
        with patch("importlib.resources.files") as m_files:
            m_files.side_effect = FileNotFoundError("Locale resource file missing")

            logger_setup = LoggerSetup("nonexistent_locale")

            self.assertEqual(logger_setup.messages, {})

    def test_handles_generic_exception(self):
        """
        Confirm that LoggerSetup safely manages unexpected exceptions during locale
        loading, ensuring the system does not fail and instead initializes with an
        empty messages dictionary, preserving stability.
        """
        with patch("importlib.resources.files") as m_files:
            m_files.side_effect = Exception("Unexpected Error")

            logger_setup = LoggerSetup("en_US")

            self.assertEqual(logger_setup.messages, {})


if __name__ == "__main__":
    unittest.main()
