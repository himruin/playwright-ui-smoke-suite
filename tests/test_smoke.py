"""smoke tests: baseline healthchecks for TodoMVC page"""

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
class TestPageLoad:
    """page load tests"""

    def test_page_title(self, default_page):
        """verify page title is correct"""
        expect(default_page).to_have_title("React • TodoMVC")

    def test_no_favicon_link(self, default_page):
        """verify page correctly has no favicon link element"""
        expect(default_page.locator("link[rel*='icon']")).to_have_count(0)


@pytest.mark.smoke
class TestFormElements:
    """page basic UI visibility tests"""

    def test_input_field_visible(self, default_page):
        """verify todo input field is present and visible"""
        expect(default_page.locator(".new-todo")).to_be_visible()

    def test_main_app_container_present(self, default_page):
        """verify main app container exists"""
        expect(default_page.locator(".todoapp")).to_be_visible()
