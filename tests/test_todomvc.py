"""integration tests: real user journeys in TodoMVC"""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
class TestTodoInteractions:
    """real task CRUD operations"""

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])  # noqa: E501
    def test_add_task(self, task_page, task_text):
        """add different tasks and verify they appear in the list"""
        task_page.add_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_be_visible()

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])  # noqa: E501
    def test_complete_task(self, task_page, task_text):
        """complete different tasks and verify visual state changes"""
        task_page.add_task(task_text)
        task_page.complete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_class("completed")  # noqa: E501

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright"])
    def test_delete_task(self, task_page, task_text):
        """delete different tasks and verify they're removed from the list"""
        task_page.add_task(task_text)
        task_page.delete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_count(0)

    @pytest.mark.parametrize(("old_text", "new_text"), [
        ("buy milk", "buy oat milk"),
        ("learn playwright", "master playwright"),
    ])
    def test_edit_task(self, task_page, old_text, new_text):
        """edit different tasks and verify they're correctly updated"""
        task_page.add_task(old_text)
        task_page.edit_task(old_text, new_text)
        expect(task_page.tasks_items.filter(has_text=old_text)).not_to_be_visible()
        expect(task_page.tasks_items.filter(has_text=new_text)).to_be_visible()

    def test_complete_workflow(self, task_page):
        """full user journey: add → edit → complete → delete"""
        task_text = "learn playwright"
        edited_text = "master playwright"

        task_page.add_task(task_text)

        task_page.edit_task(task_text, edited_text)
        expect(task_page.tasks_items.filter(has_text=edited_text)).to_be_visible()

        task_page.complete_task(edited_text)
        expect(task_page.tasks_items.filter(has_text=edited_text)).to_have_class("completed")  # noqa: E501

        task_page.delete_task(edited_text)
        expect(task_page.tasks_items.filter(has_text=edited_text)).to_have_count(0)


@pytest.mark.smoke
class TestFilters:
    """filter tab tests: All / Active / Completed"""
    def test_active_filter(self, task_page):
        task_page.add_task("buy milk")
        task_page.add_task("learn playwright")
        task_page.complete_task("buy milk")

        task_page.select_filter("Active")
        expect(task_page.tasks_items.filter(has_text="learn playwright")).to_be_visible()  # noqa: E501
        expect(task_page.tasks_items.filter(has_text="buy milk")).to_have_count(0)

    def test_completed_filter(self, task_page):
        task_page.add_task("buy milk")
        task_page.add_task("learn playwright")
        task_page.complete_task("buy milk")

        task_page.select_filter("Completed")
        expect(task_page.tasks_items.filter(has_text="buy milk")).to_be_visible()
        expect(task_page.tasks_items.filter(has_text="learn playwright")).to_have_count(0)  # noqa: E501

    def test_all_filter(self, task_page):
        task_page.add_task("buy milk")
        task_page.add_task("learn playwright")
        task_page.complete_task("buy milk")

        task_page.select_filter("Completed")
        task_page.select_filter("All")
        expect(task_page.tasks_items).to_have_count(2)
