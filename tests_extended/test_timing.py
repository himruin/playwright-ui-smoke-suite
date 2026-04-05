import pytest
from playwright.sync_api import expect


@pytest.mark.extended
def test_wait_pattern(task_page):
    task_page.add_task("learn playwright")
    # expect() retries up to the timeout (default 5s) and passes the moment the condition is met
    expect(task_page.tasks_items).to_have_count(1)