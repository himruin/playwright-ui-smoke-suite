import pytest


@pytest.fixture
def bare_page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
