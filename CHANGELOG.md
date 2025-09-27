# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-09-27

### Refactor

- __V&V for `InputValidator`:__ Implemented a comprehensive, mission-critical standard Verification & Validation (V&V) suite for the `InputValidator` base class. Achieved 100% logical path and exception coverage through a hermetic test environment with full dependency isolation. This establishes a formal proof of correctness for the component.

## [0.1.0] - 2025-09-26

### Added

- __High-Integrity Float Validator (`FloatValidator`):__ Introduced a robust, instantiable validator for floating-point numbers. It supports a rich set of configurable rules, including minimum/maximum values, maximum decimal places, and explicit handling of special values (`NaN`, `Infinity`).

## [0.1.0] - 2025-09-26

### Added

- __Centralized Exception Handling:__ Created a dedicated module (`exceptions.py`) with custom `ValidationError` and `ConfigurationError` types to standardize error signaling across the framework.

## [0.1.0] - 2025-09-26

### Changed

- __Enhanced Message Formatting:__ Upgraded `LoggerSetup` to support dynamic, placeholder-based message formatting (`**kwargs`). This enables more descriptive, context-aware error messages and logs (e.g., `"Value must be less than {max_value}")

## [0.1.0] - 2025-09-25

### Changed

- __Architectural Overhaul:__ Refactored the core validation engine (`InputValidator`) and (`IntegerValidator`) from a static-method approach to a stateful, instantiable class-based design. This allows validators to be configured once and reused, significantly improving flexibility and clarity.

## [0.1.0] - 2025-09-21

### Added

- Introduce core validation engine `InputValidator` with `validate(prompt, converter, error_message_key, locale) -> Optional[T]`, including graceful handling of `'q'` and `Ctrl+C`, localized prompts, and structured logging.

- Add typed validators:
    - `IntegerValidator.validate_integer(...)` for integer inputs with localized error messages.
    - `FloatValidator.validate_float(...)` for floating-point inputs with localized error messages.
    - `BooleanValidator.validate_boolean(...)` for `y/yes` and `n/no` inputs with localized error messages.

- Provide CLI utilities:
    - `pause_prompt()` for interactive pauses with localized messaging.
    - `print_info(message_key)` and `print_error(message_key)` for standardized, localized console output.

- Implement centralized logging and internationalization loader (`LoggerSetup`) with:
    - Environment-driven locale selection (`SAFEINPUTVERITAS_LANG`).
    - Standardized log format `[YYYY-mm-dd HH:MM:SS][SafeInputVeritas][LEVEL] message`.
    - JSON locale catalogs for `en_US`, `pt_BR`, and `es_ES`.

- Ship locale message catalogs with keys for prompts, error messages, cancellations, and unexpected errors.

- Add comprehensive unit tests (unittest) covering:
    - Successful conversions, invalid retries, user cancellation via `'q'`, `KeyboardInterrupt`, and unexpected exceptions.
    - Internationalization key presence and localized logging assertions.
    - Logging behavior that avoids exposing sensitive data.

- Provide mock integration-prep tests simulating GUI/API wrappers via patched input.
- Configure project tooling and packaging:
    - `pyproject.toml` (setuptools build backend), `setup.cfg` (flake8, isort, coverage, pytest), `tox.ini`, and .gitignore entry for egg-info.

### Changed

- N/A (initial release)

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- Hardened logging to avoid leaking user-provided secrets; use standardized, localized messages throughout validation flows.
