# Playwright UI Smoke Suite

Smoke and integration tests for TodoMVC application using Playwright. Demonstrates cross-browser testing, proper fixture design, and CI/CD integration.

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
# Run all tests (headless by default)
pytest -v

# Run with browser UI visible
pytest --headed

# Run only smoke tests
pytest tests/test_smoke.py -v

# Run specific browser
pytest -k chromium -v
```

## Structure

```
tests/              ← always runs in CI, must stay green
tests_extended/     ← signal layer: extended Playwright techniques
```

## Approach

### tests/
- **Smoke tests** (`test_smoke.py`) — Baseline healthchecks (page loads, title, UI elements present)
- **Integration tests** (`test_todomvc.py`) — Real user journeys (add todo, mark complete, delete)
- **Cross-browser** — `default_page` fixture parametrized across Chromium and Firefox

### tests_extended/
- **`test_api_mock.py`** — `page.route()` intercepts fetch calls and fulfills with mock JSON. Parametrized across drone states: IDLE, ARMED, AIRBORNE. Serves a minimal HTML fixture via route — no external server needed.
- **`test_js_runtime.py`** — `page.evaluate()` executes JavaScript in the browser and returns the result to Python. Reads `localStorage` directly to assert internal app state not visible in the DOM.
- **`test_timing.py`** — Demonstrates correct wait pattern: `expect().to_have_count()` retries until the condition is met. Contrast to `time.sleep()` which is the number one cause of flaky test suites.
- **`test_visual.py`** — Screenshot regression: captures page state before and after adding a task and asserts pixels changed. Note: `to_have_screenshot()` is JavaScript-only in Playwright — Python uses `page.screenshot()` with manual comparison.
- **`test_websocket.py`** — Registers a `framereceived` handler before navigation to capture WebSocket frames. Serves an HTML fixture that opens a real WebSocket connection to an echo server. Asserts both the DOM update and the raw captured payload.

## Run Tests

```bash
# Smoke tests only
pytest tests/ -v

# Extended tests
pytest tests_extended/ -v

# Specific browser
pytest -k chromium -v
```

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

This suite uses **synchronous Playwright** via `pytest-playwright` fixtures (`playwright`, `browser`).

**If parallelization were needed:**

For high-volume concurrent testing (100+ browsers simultaneously), async Playwright with `pytest-asyncio` would be the right choice.

**Philosophy:** Optimize for clarity first, parallelization only when needed.

## Fixture Architecture

- Root `conftest.py` — `default_page`: cross-browser (chromium + firefox), pre-navigates to TodoMVC. Uses `pytest-playwright`'s `playwright` fixture to avoid event loop conflicts.
- `tests_extended/conftest.py` — `bare_page`: chromium only, no pre-navigation. Used by tests that control their own routing and navigation.

## Test Coverage

- [x] Page load and basic UI visibility
- [x] Add todo functionality
- [x] Complete todo and state verification
- [x] Delete todo functionality
- [x] Cross-browser parametrization (Chromium, Firefox)
- [x] API mocking with parametrized drone states
- [x] JS runtime / localStorage inspection
- [x] Wait pattern contrast (correct vs flaky)
- [x] Visual regression via screenshot comparison
- [x] WebSocket interception and payload assertion

## Project Goals

- Show Playwright ecosystem expertise (fixtures, parametrized cross-browser testing, selector patterns)
- Demonstrate proper test organization with conftest and parametrization
- Real-world smoke test patterns relevant to UI QA
- CI/CD integration with GitHub Actions

## Future Enhancements

- [ ] Todo edit functionality
- [ ] Filter tests (all/active/completed)
- [x] Markers: `@pytest.mark.smoke` / `@pytest.mark.extended`
- [x] Nightly CI run at 03:00 for smoke tests
