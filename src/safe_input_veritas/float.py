"""
Float - Module for High-Integrity Floating-Point Input Validation.

This module provides the FloatValidator class, a robust component designed for the
validation of floating-point numbers in mission-critical systems. It extends the
base InputValidator to enforce a comprehensive set of constraints, including range,
precision (decimal places), and the explicit allowance of non-finite values like
Infinity and NaN.

The architectural principle is to create a configurable, stateful validator object
that applies a deterministic sequence of checks (special values, syntax, precision,
range) to ensure that only semantically and syntactically correct data proceeds
into the system's core logic. This approach embodies the fail-fast philosophy,
preventing the propagation of invalid data.

This component is fully integrated with the SafeInputVeritas internationalization
(i18n) and logging subsystems, providing clear, auditable, and localized feedback
for all validation outcomes.
"""

from __future__ import annotations

import math
from typing import Optional

from safe_input_veritas.base import InputValidator
from safe_input_veritas.exceptions import ValidationError
from safe_input_veritas.logger_config.logger_setup import get_message

__author__ = "Enock Silos"
__email__ = "init.caucasian722@passfwd.com"
__status__ = "Production-Release"


class FloatValidator(InputValidator):
    """
    Validates that an input is a floating-point number, conforming to a rich set of
    constraints.

    This class provides a comprehensive validation mechanism for floating-point
    numbers, allowing for the specification of range, precision, and handling of
    special non-finite values such as Infinity and NaN (Not a Number).
    It is designed to be instantiated with a specific configuration, enabling its
    reuse for consistent validation logic.

    The validation process is executed in a specific order to ensure fail-fast behavior:
    1.  Handling of special values (NaN, Infinity).
    2.  Syntactic validation of the numerical string format.
    3.  Precision check (number of decimal places).
    4.  Conversion to a float data type.
    5.  Semantic range validation (minimum and maximum value).

    Attributes:
        min_value (Optional[float]): The minimum acceptable value (inclusive).
        max_value (Optional[float]): The maximum acceptable value (inclusive).
        max_decimal_places (Optional[int]): The maximum number of allowed
            decimal places.
        allow_inf (bool): If True, 'inf', '-inf', 'Infinity', and '-Infinity'
            are considered valid inputs.
        allow_nan (bool): If True, 'nan' and '-nan' are considered valid inputs.
    """

    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        max_decimal_places: Optional[int] = None,
        allow_inf: bool = False,
        allow_nan: bool = False,
    ):
        """
        Initializes the FloatValidator with a specific validation configuration.

        Args:
            min_value (Optional[float]): The minimum allowed value.
            max_value (Optional[float]): The maximum allowed value.
            max_decimal_places (Optional[int]): The maximum number
                of digits after the decimal point.
            allow_inf (bool): Flag to permit infinity as a valid value.
                Defaults to False.
            allow_nan (bool): Flag to permit NaN as a valid value.
                Defaults to False.
        """
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError(
                "Configuration error: min_value cannot be greater than max_value."
            )

        self.min_value = min_value
        self.max_value = max_value
        self.max_decimal_places = max_decimal_places
        self.allow_inf = allow_inf
        self.allow_nan = allow_nan

    def validate(self, user_input: str) -> float:
        """
        Validates the user-provided string against the configured float constraints.

        Args:
            user_input (str): The input string to be validated.

        Returns:
            float: The validated floating-point number. This includes float('inf'),
                   float('-inf'), and float('nan') if they are permitted by the
                   configuration and entered by the user.

        Raises:
            ValidationError: If the input string fails any of the configured validation
                checks. The exception message is internationalized.
        """
        normalized_input = user_input.strip().lower()

        if normalized_input in ("nan", "-nan"):
            if self.allow_nan:
                return float("nan")
            else:
                raise ValidationError(get_message("error_nan_not_allowed"))

        if normalized_input in ("inf", "infinity", "-inf", "-infinity"):
            if self.allow_inf:
                return (
                    float("inf")
                    if not normalized_input.startswith("-")
                    else float("-inf")
                )
            else:
                raise ValidationError(get_message("error_inf_not_allowed"))

        try:
            numeric_value = float(user_input)
        except ValueError:
            raise ValidationError(get_message("error_float")) from None

        if self.max_decimal_places is not None and not math.isinf(numeric_value):
            if "." in user_input:
                decimal_part = user_input.strip().split(".")[-1].lower().split("e")[0]

                if len(decimal_part) > self.max_decimal_places:
                    raise ValidationError(
                        get_message(
                            "error_max_decimal_places",
                            max_places=self.max_decimal_places,
                        )
                    )

        if self.min_value is not None and numeric_value < self.min_value:
            raise ValidationError(
                get_message("error_min_value", min_value=self.min_value)
            )

        if self.max_value is not None and numeric_value > self.max_value:
            raise ValidationError(
                get_message("error_max_value", max_value=self.max_value)
            )

        return numeric_value
