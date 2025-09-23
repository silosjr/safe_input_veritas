# __SafeInputVeritas__

Secure, auditable, and extensible user input validation for Python CLI.

## __Overview__

SafeInputVeritas centralizes user input acquisition and validation with a zero-trust engine, localized messaging (`en_US`, `pt_BR`, `es_ES`), and structured logging designed for auditability and production reliability. It delivers predictable control flow through `Optional` returns, graceful handling of `'q'` and `Ctrl+C`, and strong guarantees around non-disclosure of sensitive data in logs.

### __Why this project__

- Enforces consistent, reusable validation across scripts and services.
- Provides internationalization first prompts and errors with JSON catalogs.
- Ensures audit-friendly logging with deterministic, actionable messages.
- Prioritizes security and reliability from mission-critical CLI environments.

### __Key features__

- Generic validation engine + typed wrappers (`int`, `float`, `bool`).
- Internationalization (`en_US`, `pt_BR`, `es_ES`) with locale selection at runtime.
- Structured logging at `INFO`/`WARNING`/`ERROR` with no secrets leakage.
- Graceful cancellations returning `None` instead of raising to callers.
- High testability and CI-friendly coverage targets.

### __Quick start__

#### __Installation__
- Python 3.8+ recommended.
- From a virtual environment:
    - `pip install -e .`

### __Validate an integer__

```python
from safe_input_veritas.integer import IntegerValidator

value = IntegerValidator.validate_integer(
    prompt='Enter an integer: ',
    locale='en_US'
)
if value is None:
    # Handle user cancellation (e.g., Ctrl+C or 'q')
    ...
else:
    # Use the validated integer
    ...
```

### __Locale selection__

- Explicit per call: pass `locale='pt_BR'` or `'es_ES'`.
- Or set the environment variable: `SAFEINPUTVERITAS_LANG=pt_BR`

### __Next steps__

- Usage guide: Learn the typed validators, generic conversions, and best practices.
- How‑to guides: Add new validators, extend locales, and harden logging policies.
- API reference: Function signatures, return contracts, and error keys.
- Concepts & design: Security posture, i18n architecture, and logging strategy.
- Internationalization: Message catalogs, required keys, and translation tips.
- Logging: Levels, formatting, and guidance to avoid sensitive data exposure.
- Testing: Running tests, coverage goals (≥95%), and stress scenarios.
- Integration: Patterns for GUI/API wrappers and non‑CLI environments.

### __Project status__

- Current version: 0.1.0. See the Changelog for release notes.

### __Requirements__

- Python 3.8+ and recent version of pip.

### __License__
- MIT License. See the LICENSE file for details.
