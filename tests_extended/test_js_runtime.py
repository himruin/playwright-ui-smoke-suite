import json
import pytest
from playwright.sync_api import expect


@pytest.mark.extended
def test_todo_stored_in_localstorage(default_page):
    task_input = default_page.locator(".new-todo")
    task_input.fill("learn playwright")
    task_input.press("Enter")

    # discover all localStorage keys -> react-todos
    keys = default_page.evaluate("() => Object.keys(localStorage)")
    print(keys)

    # reads localStorage via JS
    raw = default_page.evaluate("() => localStorage.getItem('react-todos')")
    tasks = json.loads(raw)
    assert len(tasks) == 1
    assert tasks[0].get("title") == "learn playwright"
    assert tasks[0].get("completed") is False