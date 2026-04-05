from playwright.sync_api import Page, Locator

# POM
class TaskPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = base_url

        self.new_task: Locator = page.locator("input.new-todo")

        # playwright returns collection of li elements (each task - 1 element)
        self.tasks_items: Locator = page.get_by_test_id("todo-item")

        self.task_count: Locator = page.locator(".todo-count")
        self.toggle_all: Locator = page.locator("#toggle-all") #catch by ID selector

    def add_task(self, task_text: str) -> None:
        self.new_task.fill(task_text)
        self.new_task.press("Enter")

    def _task_item(self, task_text: str) -> Locator:
        return self.tasks_items.filter(has_text=task_text)

    def complete_task(self, task_text: str) -> None:
        self._task_item(task_text).locator(".toggle").click()
 
    def delete_task(self, task_text: str) -> None:
        item = self._task_item(task_text)
        item.hover()
        item.locator(".destroy").click()