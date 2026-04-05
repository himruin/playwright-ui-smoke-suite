"""smoke tests: baseline healthchecks for TodoMVC page"""

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
class TestPageLoad:
    """page load tests"""

    def test_page_title(self, task_page):
        """verify page title is correct"""
        expect(task_page.page).to_have_title("React • TodoMVC")

    def test_no_favicon_link(self, task_page):
        """verify page correctly has no favicon link element"""
        expect(task_page.page.locator("link[rel*='icon']")).to_have_count(0)


@pytest.mark.smoke
class TestFormElements:
    """page basic UI visibility tests"""

    def test_input_field_visible(self, task_page):
        """verify todo input field is present and visible"""
        expect(task_page.new_task).to_be_visible()

    def test_main_app_container_present(self, task_page):
        """verify main app container exists"""
        expect(task_page.page.locator(".todoapp")).to_be_visible()
