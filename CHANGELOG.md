# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
