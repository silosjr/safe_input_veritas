# __Usage__
This guide shows how to install, configure, and use SafeInputVeritas for secure, auditable, and localized CLI input validation.

## __Requirements__
- Python 3.8+.
- A virtual environment is recommended.

## __Installation__
- From source:
    - `python -m venv .venv && source .venv/bin/activate`
    - `pip install -e .`

## __Concepts at a glance__
- Generic engine: `InputValidator.validate(prompt, converter, error_message_key, locale) -> Optional[T]`.
- Typed wrappers: `IntegerValidator`, `FloatValidator`, `BooleanValidator`.
- Internationalization (i18n): locale-driven messages (`en_US`, `pt_BR`, `es_ES`).
- Structured logging: `INFO` for cancellations, `WARNING` for invalid input, `ERROR` for unexpected exceptions.
- Predictable control flow: returns a value or `None` (on `'q'` or `Ctrl+C`).

### __Integer input__
Validate and convert integers with localized error and graceful cancellation.
```python
from safe_input_veritas.integer import IntegerValidator

n = IntegerValidator.validate_integer(
    prompt='Enter an integer: ',
    locale='en_US'
)
if n is None:
    # User cancelled with 'q' or Ctrl+C
    ...
else:
    print(f'Integer: {n}')
```
#### __Notes__

- *On invalid input, the user is re-prompted with a localized error message*.
- On `'q'` or `Ctrl+C`, returns `None` and logs an info-level event.

### __Float input__

Validate and convert floats, including scientific notation.
```python
from safe_input_veritas.float import FloatValidator

x = FloatValidator.validate_float(
    prompt='Enter a float: ',
    locale='en_US'
)
if x is None:
    ...
else:
    print(f'Float: {x}')
```

### __Boolean input__

Accepts y/yes and n/no (*case-insensitive*) and converts to bool.
```python
from safe_input_veritas.boolean import BooleanValidator

ok = BooleanValidator.validate_boolean(
    prompt='Proceed? (y/n): ',
    locale='en_US'
)
if ok is None:
    ...
elif ok:
    print('Continuing...')
else:
    print('Aborted')
```

### __Generic validation__

Plug any *callable* converter that raises `ValueError` on invalid input.
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
if port is None:
    ...
```
#### __Best Practices__

- Keep converters pure and deterministic.
- Raise `ValueError` for invalid inputs.
- Select an `error_message_key` that matches the input domain.

### __Localization (i18n)__

Use an explicit locale or set an environment variable.
- Per call: pass `locale='pt_BR'` or `'es_ES'`.
- Environment: `SAFEINPUTVERITAS_LANG=pt_BR`

### __Messages keys (non-exhaustive)__

- `'user_interrupted'`, `'unexpected_error'`, `'invalid_input'`
- `'cancel_prompt'`, `'pause_prompt'`, `'input_prompt'`
- `'error_integer'`, `'error_float'`, `'error_boolean'`
- `'converter_none_error'`

### __Logging__

- Logger: `SafeInputVeritas`
- Format: `[YYYY-mm-dd HH:MM:SS][SafeInputVeritas][LEVEL] message`.
- Levels:
    - `INFO`: cancellations, lifecycle.
    - `WARNING`: invalid inputs and retries.
    - `ERROR`: unexpected exceptions.
- Do not log raw user inputs from converters; use localized messages.

### __CLI utilities__

Standardized helpers integrated with i18n and logging.
```python
from safe_input_veritas.cli_utils import pause_prompt, print_info, print_error

print_info('input_prompt')              # Prints localized prompt and logs INFO
print_error('invalid_input')            # Prints localized error and logs ERROR
pause_prompt()                          # 'Press Enter to continue...' and waits
```

### __Behavioral contracts__

- Returns converted value on success.
- Return None on `'q'` or `Ctrl+C` (no exceptions are propagated for cancellations).
- On conversion error (`ValueError`), the user is re-prompted until valid or cancel.
- On unexpected exceptions, logs `ERROR` and returns `None`.

#### __Troubleshooting__

- No output or unexpected locale.
    - Ensure `SAFEINPUTVERITAS_LANG` is set correctly or pass locale *explicitly*.
- Re-prompts indefinitely:
    - Verify the converter raises `ValueError` for invalid input and that `error_message_key` exists in the locale.
- Sensitive data in logs:
    Remove any logging of raw user input from custom converters. The framework avoids it by design.

##### __Examples__

###### __*Range-constrained integer*__
```python
from safe_input_veritas.base import InputValidator

def positive_int(s: str) -> int:
    v = int(s)
    if v > 0:
        return v
    raise ValueError('not positive')

res = InputValidator.validate(
    prompt='Enter a positive integer: ',
    converter=positive_int,
    error_message_key='error_integer',
    locale='en_US'
)
```

###### __*Boolean with extended aliases*__
```python
from safe_input_veritas.base import InputValidator

def yes_no(s: str) -> bool:
    v = s.strip().lower()
    if v in ('y', 'yes', 'true', 't', '1'):
        return True
    if v in ('n', 'no', 'false', 'f', '0'):
        return False
    raise ValueError('invalid')

ans = InputValidator.validate(
    prompt='Proceed? ',
    converter=yes_no,
    error_message_key='error_boolean',
    locale='en_US'
)
```

### __Testing__
- Run tests:
    - `pytest -q`
- Coverage target:
    - Minimum 95% configured in `setup.cfg`.
- Typical scenarios:
    - Valid conversions, invalid retries, `'q'`, `Ctrl+C`, unexpected exceptions, i18n presence, and no sensitive data in logs.

### __Integration patterns__
- GUI: capture input via UI elements, pass strings to validators, handle `None` for cancellations.
- APIs: sanitize and map request strings to converters; return localized messages for client feedback if appropriate.

### __Versioning and changelog__
- Semantic Versioning. See `CHANGELOG.md` for release notes.

### __License__
- MIT License. See `LICENSE`.
