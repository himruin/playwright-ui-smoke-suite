import pytest


@pytest.mark.extended
def test_visual_state_changes(task_page):
    before = task_page.page.screenshot()

    task_page.add_task("learn playwright")

    after = task_page.page.screenshot()
    assert before != after  # pixels changed after adding task
