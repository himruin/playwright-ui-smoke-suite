import json
import pytest
from playwright.sync_api import expect


@pytest.mark.extended
def test_todo_stored_in_localstorage(task_page):
    task_page.add_task("learn playwright")

    # discover all localStorage keys -> react-todos
    keys = task_page.page.evaluate("() => Object.keys(localStorage)")
    print(keys)

    # reads localStorage via JS
    raw = task_page.page.evaluate("() => localStorage.getItem('react-todos')")
    tasks = json.loads(raw)
    assert len(tasks) == 1
    assert tasks[0].get("title") == "learn playwright"
    assert tasks[0].get("completed") is False