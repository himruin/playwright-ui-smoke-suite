# Playwright UI Smoke Suite

Smoke and integration tests for TodoMVC application using Playwright. Demonstrates POM architecture, cross-browser testing, fixture design, and CI/CD integration.

## Target

**URL:** https://demo.playwright.dev/todomvc

Official Playwright demo — maintained by the Playwright team, no login required, real UI interactions (add/complete/delete todos).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium firefox
```

## Run Tests

```bash
# Smoke tests only (always green in CI)
pytest -m smoke -v

# Extended tests
pytest -m extended -v

# All tests
pytest -v

# Run with browser UI visible
pytest --headed

# Override browser
pytest --browser chromium -v
```

## Project Structure

```
pages.py                ← POM: TaskPage class, all locators and actions
conftest.py             ← task_page fixture (wraps TaskPage + navigation)
pytest.ini              ← base_url, cross-browser addopts, marker definitions
tests/
    test_smoke.py       ← baseline healthchecks, always runs in CI
    test_todomvc.py     ← CRUD user journeys via TaskPage POM
tests_extended/
    conftest.py         ← bare_page fixture for route-controlled tests
    test_api_mock.py    ← page.route() fetch interception
    test_js_runtime.py  ← page.evaluate() / localStorage inspection
    test_timing.py      ← correct wait pattern vs time.sleep()
    test_visual.py      ← screenshot regression
    test_websocket.py   ← WebSocket frame capture
```

## Architecture

### Page Object Model — `pages.py`

All TodoMVC locators and actions live in `TaskPage`. Tests never use raw locators.

```python
task_page.add_task("buy milk")
task_page.complete_task("buy milk")
task_page.delete_task("buy milk")
```

`task_page` fixture in `conftest.py` navigates to `base_url` and returns `TaskPage(page, base_url)`. Tests that need a blank page (route mocking, WebSocket) use `bare_page` from `tests_extended/conftest.py` instead.

### Cross-browser

`pytest.ini` sets `addopts = --browser chromium --browser firefox` — all tests run on both browsers automatically with no per-test changes.

### Marker Strategy

| Marker | Scope | CI behaviour |
|---|---|---|
| `smoke` | `tests/` | Runs on every push and PR |
| `extended` | `tests_extended/` | Runs after smoke passes (`needs: smoke`) |

## Tests — Extended Layer

- **`test_api_mock.py`** — `page.route()` intercepts fetch calls and fulfills with mock JSON. Parametrized across drone states: IDLE, ARMED, AIRBORNE. Serves a minimal HTML fixture via route — no external server needed.
- **`test_js_runtime.py`** — `page.evaluate()` executes JavaScript in the browser and returns the result to Python. Reads `localStorage` directly to assert internal app state not visible in the DOM.
- **`test_timing.py`** — Demonstrates correct wait pattern: `expect().to_have_count()` retries until the condition is met. Contrast to `time.sleep()` which is the number one cause of flaky test suites.
- **`test_visual.py`** — Screenshot regression: captures page state before and after adding a task and asserts pixels changed.
- **`test_websocket.py`** — Registers a `framereceived` handler before navigation to capture WebSocket frames. Serves an HTML fixture that opens a real WebSocket connection to an echo server. Asserts both the DOM update and the raw captured payload.

## Docker

```bash
# Build
docker build -t playwright-suite .

# Run smoke tests (default)
docker run --rm playwright-suite

# Run extended tests
docker run --rm playwright-suite pytest tests_extended/ -m extended --tb=short
```

## Design Decision: Sync vs Async

This suite uses **synchronous Playwright** via `pytest-playwright` fixtures. Browser lifecycle (launch, context, page, teardown) is managed automatically by the built-in `page` fixture.

For high-volume concurrent testing (100+ browsers simultaneously), async Playwright with `pytest-asyncio` would be the right choice.

**Philosophy:** Optimize for clarity first, parallelization only when needed.

## Test Coverage

- [x] Page load and basic UI visibility
- [x] Add / complete / delete task via POM
- [x] Cross-browser parametrization (Chromium, Firefox)
- [x] API mocking with parametrized drone states
- [x] JS runtime / localStorage inspection
- [x] Wait pattern (expect retry vs time.sleep)
- [x] Visual regression via screenshot comparison
- [x] WebSocket interception and payload assertion
- [x] CI/CD with GitHub Actions (smoke → extended pipeline)
- [x] Docker support

## Future Enhancements

- [ ] Task edit functionality
- [ ] Filter tests (all / active / completed)
- [ ] Failure screenshots as CI artifacts
