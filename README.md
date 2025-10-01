# __SafeInputVeritas__
Secure, auditable, and extensible user input validation framework for Python CLI applications.

## __Overview__
__SafeInputVeritas__ centralizes user input handling for command-line applications with a robust, zero-trust validation engine, internationalized messaging (i18n), and structured logging designed for auditability and production reliability. It enforces strict, reusable validation with graceful cancellation and predictable control flow for security-sensitive environments.

## __Key Features__
- Object-oriented validation core with a generic engine and typed wrappers (`int`, `float`, `bool`).
- Internationalization for prompts and errors (*en_US*, *pt_BR*, *es_ES*), with locale-driven messages.
- Structured logging (`INFO`, `WARNING`, `ERROR`) with deterministic, audit-friendly entries and no secrets leakage.
- Graceful cancellation via `Ctrl+C` and `'q'`, returning `Optional` results instead of raising.
- High testability with deterministic behavior and coverage targets suitable for *CI*/*CD*.

## __Why *SafeInputVeritas*__
*Ad-hoc* input validation is error-prone and inconsistent across scripts and services. __*SafeInputVeritas*__ offers a uniform, auditable, and extensible approach that adheres to *secure-by-default* practices, supporting predictable outcomes, localization, and comprehensive logging in *mission-critical scenarios*.

## __Design Principles__
- *Zero Trust* input handling.
- Separation of concerns: validation, I/O, localization, logging.
- Extensibility through pluggable converters and typed wrappers.
- Deterministic control flow with `Optional` returns on all paths.
- *Internationalization first*: no hardcoded UI strings.

## __Architecture__
### __Core__: `InputValidator`
- `validate(prompt: str, converter: Optional[Callable[[str], T]], error_message_key: str, locale: Optional[str] = None) -> Optional[T]`
- Repeats input until valid or canceled, applies converter, handles exceptions.
### __Typed Wrappers__
- `IntegerValidator.validate_integer(...)`
- `FloatValidator.validate_float(...)`
- `BooleanValidator.validate_boolean(...)`
### __CLI Utilities__
- `pause_prompt()`, `print_info(key)`, `print_error(key)`
### __Logging and i18n__
- Central logger with consistent format and levels.
- Locale `JSON` catalogs loaded at runtime, overridable environment variable `SAFEINPUTVERITAS_LANG`.

## __Security Posture__
- Defensive validation prior to processing.
- No sensitive data exposure in logs.
- Controlled failure modes: `None` on user cancel; no uncaught exceptions on cancellation paths.
- Comprehensive logging suitable for audits and forensics.

## __Internationalization (i18n)__
- Supported locales: *en_US*, *pt_BR*, *es_ES*.
- All prompts and error messages stored in locale `JSON` *files*.
### __Locale selection:__
- Explicit: pass locale to API calls.
- Environment: `SAFEINPUTVERITAS_LANG`.
- Adding a locale: provide `{locale}.json` with the same keys and register the code.

## __Public API__
### __Core__
- `InputValidator.validate(prompt: str, converter: Callable[[str], T], error_message_key: str, locale: Optional[str] = None) -> Optional[T]`
### __Wrappers__
- `IntegerValidator.validate_integer(prompt: str='', locale: Optional[str] = None) -> Optional[int]`
- `FloatValidator.validate_float(prompt: str='', locale: Optional[str] = None) -> Optional[float]`
- `BooleanValidator.validate_boolean(prompt: str='', locale: Optional[str] = None) -> Optional[bool]`
### __CLI utils__
- `pause_prompt() -> None`
- `print_info(message_key: str) -> None`
- `print_error(message_key: str) -> None`

## __Behavioral Contracts__
- Valid input returns the converted value.
- `'q'` or `Ctrl+C` returns `None`.
- Conversion errors produce a localized error message and re-prompt.
- Unexpected exceptions are logged and result in `None`; callers are not crashed.
- Logging is standardized and localized; messages never include raw user inputs.

## __Installation__
- Prerequisites: *Python 3.8+*
- From source:
    - Create and activate a virtual environment.
    - `pip install -e .`
- Packaging:
    - Configured via `pyproject.toml` (*setuptools build backend*).

## __Quick Start__

### __*Integers*__
```python
from safe_input_veritas.integer import IntegerValidator

value = IntegerValidator.validate_integer(
    prompt='Enter an integer: ',
    locale='en_US'
)
if value is None:
    # Handle user cancellation gracefully
    ...
```

### __*Floats*__
```python
from safe_input_veritas.float import FloatValidator

value = FloatValidator.validate_float(
    prompt='Enter a floating-point number: ',
    locale='en_US'
)
```

### __*Booleans*__
```python
from safe_input_veritas.boolean import BooleanValidator

value = BooleanValidator.validate_boolean(
    prompt='Proceed? (y/n): ',
    locale='en_US'
)
if value:
    ...
```

### __*Generic Validation*__
```python
from safe_input_veritas.base import InputValidator

def to_upper(s: str) -> str:
    v = s.strip()
    if not v:
        raise ValueError('empty')
    return v.upper()

res = InputValidator.validate(
    prompt='Enter a value: ',
    converter=to_upper,
    error_message_key='invalid_input',
    locale='pt_BR'
)
```

## __Localization Usage__
- Default locale: *en_US*
- Select at runtime:
    - Environment: `SAFEINPUTVERITAS_LANG=pt_BR`
    - Explicit: pass `locale='es_ES'` to API calls.
- Message keys (non-exhaustive):
    - `'user_interrupted'`, `'unexpected_error'`, `'invalid_input'`
    - `'cancel_prompt'`, `'pause_prompt'`, `'input_prompt'`
    - `'error_integer'`, `'error_float'`, `'error_boolean'`
    - `'converter_none_error'`

## __Logging__
- Logger name: `SafeInputVeritas`
- Format: `[YYYY-mm-dd HH:MM:SS][SafeInputVeritas][LEVEL] message`
- Levels:
    - `INFO`: User cancellations and lifecycle notices.
    - `WARNING`: Invalid input and recoverable validation events.
    - `ERROR`: Unexpected errors and exception details.
- Best Practices:
    - Do not log raw user inputs in converters.
    - Use localized message keys for consistency and determinism.

## __Return and Error Handling Matrix__
- Valid input: converted value (e.g., `int`, `float`, `bool`, `str`).
- Invalid input: warning logged; localized error printed; re-prompt.
- `'q'`: info logged; returns `None`.
- `Ctrl+C`: info logged; new line printed; returns `None`.

## __Usage Patterns and Best Practices__
- Always branch on `None` to handle cancellations predictably.
- Specify locale explicitly in deterministic or compliance-sensitive contexts.
- Choose the correct `error_message_key` per converter type.
- For domain constraints (ranges, regex), encapsulate logic inside the converter and raise `ValueError` on failure.

## __Extensibility__
- New typed validators: compose `InputValidator.validate` with a custom converter and error message key.
- Complex strategies: implement domain-specific converters (e.g., ranges, CIDR, enums) using *Strategy*.
- Additional locales: add `JSON` catalogs maintaining key parity across languages.

## __Testing Strategy__
- Unit tests cover:
    - Valid conversions, retries, `'q'` cancel, `Ctrl+C` handling, unexpected exceptions.
    - i18n key presence across locales and log localization.
    - No sensitive data in logs.
- Mock-integration tests simulate GUI/API wrappers via patched input.
- Coverage target: 95%+.

## __Project Layout__
```text
src/safe_input_veritas/
  base.py                               # Core validation engine
  integer.py, float.py, boolean.py      # Typed wrappers
  cli_utils.py                          # CLI helpers with i18n/logging
  logger_config/logger_setup.py         # Central logging + i18n loader
  locales/                              # en_US.json, pt_BR.json, es_ES.json
tests/                                  # Unit and integration-prep tests
docs/                                   # Documentation (index, usage)
pyproject.toml, setup.cfg               # Packaging and tooling
```

## __Configuration and Conventions__
- Style: PEP 8.
- Tooling: flake8, isort (Black profile), coverage thresholds aligned with CI gates.
- Tests: unittest-based with patching of input and logger calls.

### __*Examples*__
#### __*Port number*__ *(range constraint)*
```python
from safe_input_veritas.base import InputValidator

def port_converter(s: str) -> int:
    p = int(s)
    if 1 <= p <= 65535:
        return p
    raise ValueError('invalid port')

port = InputValidator.validate(
    prompt='Enter port: ',
    converter=port_converter,
    error_message_key='error_integer',
    locale='en_US'
)
```

#### __*Boolean with extended aliases*__
```python
from safe_input_veritas.base import InputValidator

def yes_no(s: str) -> bool:
    v = s.strip().lower()
    if v in ('y', 'yes', 'true', 't', '1'):
        return True
    if v in ('n', 'no', 'false', 'f', '0'):
        return False
    raise ValueError('invalid boolean')

ans = InputValidator.validate(
    prompt='Proceed? :',
    converter=yes_no,
    error_message_key='error_boolean',
    locale='en_US'
)
```

## __Compliance and Practices__
- Aligned with secure coding and operational practices common to __PESSMC__-*alike structural standards*, __NIST Cybersecurity Framework__, __OWASP Top Ten__ considerations, and __DevSecOps__ workflows for traceability and auditability.

## __Roadmap__
- Additional built-in validators (*decimal*, *date*/*time*, *enums*).
- Rich constraints (*ranges*, *regex*, *combinators*).
- Async adapters and non-blocking input strategies.
- Pluggable logging sinks and metric exporters.
- Extended locales and runtime locale negotiation.

## __Contributing__
- Propose changes with clear rationale and tests.
- Maintain i18n key parity across all locales.
- Adhere to style, logging, and *Optional return* contracts.
- Avoid logging sensitive or user-provided raw values.

## __License__
MIT License. See LICENSE for details.

## __Acknowledgments__
`SafeInputVeritas` by Enock Silos, designed for security-sensitive environments and production-grade auditability.
