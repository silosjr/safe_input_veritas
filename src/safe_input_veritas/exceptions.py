"""
exceptions - Custom exceptions for the SafeInputVeritas framework.

This module defines a set of custom exception types that are used throughout the
framework to signal specific error conditions. Using custom exceptions allows client
code to build robust error handling logic by catching specific failure modes from the
validation process.
"""

from __future__ import annotations

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Release"


class ConfigurationError(Exception):
    """
    Custom exception for critical configuration failures.
    """

    pass


class ValidationError(Exception):
    """
    Exception raised for errors during the input validation process.

    This exception is raised when the user input fails to conform to any the rules
    defined by the specific validator instance being used. The exception message
    should be a clear, user-facing, and internationalized explanation of the failure.
    """

    pass
