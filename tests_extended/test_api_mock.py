import pytest
from playwright.sync_api import expect

HTML_FIXTURE = """
    <!DOCTYPE html>
    <html>
    <body>
        <div id="status">loading...</div>
        <script>
        fetch("/api/drone/status")
            .then(r => r.json())
            .then(data => {
            document.getElementById("status").textContent = data.state;
            });
        </script>
    </body>
    </html>
"""

@pytest.mark.extended
@pytest.mark.parametrize("state", ["IDLE", "ARMED", "AIRBORNE"])
def test_drone_state_display(bare_page, state):
    bare_page.route("**/", lambda route: route.fulfill(status=200, content_type="text/html", body=HTML_FIXTURE))
    bare_page.route("**/api/drone/status", lambda route: route.fulfill(status=200, content_type="application/json", body=f'{{"state":"{state}"}}'))
    bare_page.goto("http://test.local/")
    # bare_page.pause()
    # bare_page.screenshot(path="debug.png")
    expect(bare_page.locator("#status")).to_have_text(state)