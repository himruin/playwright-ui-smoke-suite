FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps chromium firefox

COPY . .

CMD ["pytest", "tests/", "-m", "smoke", "--tb=short"]
