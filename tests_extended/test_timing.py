import pytest
from playwright.sync_api import expect

@pytest.mark.extended
def test_wait_pattern(default_page):
    default_page.locator(".new-todo").fill("learn playwright")
    default_page.locator(".new-todo").press("Enter")
    # expect() retries up to the timeout (default 5s) and passes the moment the condition is met
    expect(default_page.get_by_test_id("todo-item")).to_have_count(1)