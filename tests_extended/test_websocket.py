import pytest
from playwright.sync_api import expect

HTML_FIXTURE = """
    <!DOCTYPE html>
    <html>
    <body>
        <script>
            const ws = new WebSocket("wss://echo.websocket.org");
            ws.onopen = () => ws.send("drone-1 present");
            ws.onmessage = (e) => {
            document.getElementById("message").textContent = e.data;
            };
        </script>
        <div id="message"></div>
    </body>
    </html>
"""


@pytest.mark.extended
def test_websocket_echo(bare_page):
    received = []
    bare_page.on(
        "websocket",
        lambda ws: ws.on("framereceived", lambda payload: received.append(payload)),
    )
    bare_page.route(
        "**/",
        lambda route: route.fulfill(
            status=200, content_type="text/html", body=HTML_FIXTURE
        ),
    )
    bare_page.goto("http://test.local/")
    expect(bare_page.locator("#message")).to_have_text("drone-1 present")
    assert "drone-1 present" in received
