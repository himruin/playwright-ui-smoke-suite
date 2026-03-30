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

## Approach

- **Smoke tests** (`test_smoke.py`) — Baseline healthchecks (page loads, title, UI elements present)
- **Integration tests** (`test_todomvc.py`) — Real user journeys (add todo, mark complete, delete)
- **Cross-browser** — Parametrized fixtures run tests on Chromium and Firefox
- **CI-ready** — standard pytest output, easy to integrate into any CI pipeline

## Design Decision: Sync vs Async

**Why Sync Playwright?**

This suite uses **synchronous Playwright** because:
- Smoke tests don't require concurrency (not running 100+ parallel browsers)
- Synchronous code is clearer and more maintainable for straightforward test flows
- No async/await boilerplate overhead for sequential UI interactions
- Standard approach for most production test suites

**If parallelization were needed:**

For high-volume concurrent testing (100+ browsers simultaneously), async Playwright with `pytest-asyncio` would be the right choice:
```python
from playwright.async_api import async_playwright
import pytest

@pytest.fixture
async def page(browser_type):
    async with async_playwright() as p:
        browser = await getattr(p, browser_type).launch()
        page = await browser.new_page()
        await page.goto("https://demo.playwright.dev/todomvc")
        yield page
        await page.close()
```

**Philosophy:** Optimize for clarity first, parallelization only when needed.

## Test Coverage

- [x] Page load and basic UI visibility
- [x] Add todo functionality
- [x] Complete todo and state verification
- [x] Delete todo functionality
- [x] Cross-browser parametrization (Chromium, Firefox)

## Project Goals

- Show Playwright ecosystem expertise (fixtures, parametrized cross-browser testing, selector patterns)
- Demonstrate proper test organization with conftest and parametrization
- Real-world smoke test patterns relevant to UI QA
- CI/CD integration with GitHub Actions

## Future Enhancements

- [ ] Todo edit functionality
- [ ] Filter tests (all/active/completed)
- [ ] Performance metrics collection
- [ ] Screenshot on failure
