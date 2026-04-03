import pytest

@pytest.mark.extended
def test_visual_state_changes(page, base_url):
    page.goto(base_url)
    before = page.screenshot()

    page.locator(".new-todo").fill("learn playwright")
    page.locator(".new-todo").press("Enter")

    after = page.screenshot()
    assert before != after  # pixels changed after adding task