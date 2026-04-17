"""Pytest configuration and fixtures for Playwright tests

Using synchronous Playwright for clarity and simplicity.
Browser lifecycle (launch, context, page, teardown) is managed automatically
by the pytest-playwright built-in `page` fixture — equivalent sync implementation:

    @pytest.fixture
    def page(playwright, browser_type, base_url):
        browser = getattr(playwright, browser_type).launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(base_url)
        yield page
        context.close()
        browser.close()

For high-volume parallel testing (e.g. 100+ concurrent browsers),
using async Playwright with pytest-asyncio recommended instead:

    from playwright.async_api import async_playwright

    @pytest.fixture
    async def page(browser_type):
        async with async_playwright() as p:
            browser = await getattr(p, browser_type).launch()
            page = await browser.new_page()
            await page.goto("https://demo.playwright.dev/todomvc")
            yield page
            await page.close()
"""

import pytest
from pages import TaskPage


@pytest.fixture
def task_page(page, base_url):
    page.goto(base_url)
    return TaskPage(page, base_url)
