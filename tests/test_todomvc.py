"""integration tests: real user journeys in TodoMVC"""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
class TestTodoInteractions:
    """real task CRUD operations"""

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])
    def test_add_task(self, task_page, task_text):
        """add different tasks and verify they appear in the list"""
        task_page.add_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_be_visible()

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])
    def test_complete_task(self, task_page, task_text):
        """complete different tasks and verify visual state changes"""
        task_page.add_task(task_text)
        task_page.complete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_class("completed")

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright"])
    def test_delete_task(self, task_page, task_text):
        """delete different tasks and verify they're removed from the list"""
        task_page.add_task(task_text)
        task_page.delete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_count(0)

    def test_complete_and_delete_workflow(self, task_page):
        """full user journey: add → complete → delete"""
        task_text = "learn playwright"

        task_page.add_task(task_text)
        task_page.complete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_class("completed")

        task_page.delete_task(task_text)
        expect(task_page.tasks_items.filter(has_text=task_text)).to_have_count(0)
