"""integration tests: real user journeys in TodoMVC"""
import pytest
from playwright.sync_api import expect


class TestTodoInteractions:
    """real task CRUD operations"""

    def add_task(self, page, task_text):
        """helper: add a task to the list"""
        todo_input = page.locator(".new-todo")
        todo_input.fill(task_text)
        todo_input.press("Enter")

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])
    def test_add_task(self, page, task_text):
        """add different tasks and verify they appear in the list"""
        self.add_task(page, task_text)
        expect(page.locator("li").filter(has_text=task_text)).to_be_visible()

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright", "code review"])
    def test_complete_task(self, page, task_text):
        """complete different tasks and verify visual state changes"""
        self.add_task(page, task_text)

        task_item = page.locator("li").filter(has_text=task_text)
        task_item.locator(".toggle").click()

        expect(task_item).to_have_class("completed")

    @pytest.mark.parametrize("task_text", ["buy milk", "learn playwright"])
    def test_delete_task(self, page, task_text):
        """delete different tasks and verify they're removed from the list"""
        self.add_task(page, task_text)

        task_item = page.locator("li").filter(has_text=task_text)
        task_item.hover()
        task_item.locator(".destroy").click()

        expect(page.locator("li").filter(has_text=task_text)).to_have_count(0)

    def test_complete_and_delete_workflow(self, page):
        """full user journey: add → complete → delete"""
        task_text = "learn playwright"

        # add a task
        self.add_task(page, task_text)
        task_item = page.locator("li").filter(has_text=task_text)

        # complete the task
        task_item.locator(".toggle").click()
        expect(task_item).to_have_class("completed")

        # delete the completed task
        task_item.hover()
        task_item.locator(".destroy").click()
        expect(page.locator("li").filter(has_text=task_text)).to_have_count(0)
