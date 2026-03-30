"""Pytest configuration and fixtures for Playwright tests

Using synchronous Playwright for clarity and simplicity.
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
from playwright.sync_api import sync_playwright


@pytest.fixture(params=["chromium", "firefox"])
def browser_type(request):
    """parametrize tests to run on Chromium and Firefox"""
    return request.param


@pytest.fixture
def page(browser_type):
    """create a Playwright page fixture with base URL"""
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://demo.playwright.dev/todomvc")

        yield page

        context.close()
        browser.close()
