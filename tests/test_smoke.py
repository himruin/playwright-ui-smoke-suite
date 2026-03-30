"""smoke tests: baseline healthchecks for TodoMVC page"""

from playwright.sync_api import expect


class TestPageLoad:
    """page load tests"""

    def test_page_title(self, page):
        """verify page title is correct"""
        expect(page).to_have_title("React • TodoMVC")

    def test_no_favicon_link(self, page):
        """verify page correctly has no favicon link element"""
        expect(page.locator("link[rel*='icon']")).to_have_count(0)


class TestFormElements:
    """page basic UI visibility tests"""

    def test_input_field_visible(self, page):
        """verify todo input field is present and visible"""
        expect(page.locator(".new-todo")).to_be_visible()

    def test_main_app_container_present(self, page):
        """verify main app container exists"""
        expect(page.locator(".todoapp")).to_be_visible()
