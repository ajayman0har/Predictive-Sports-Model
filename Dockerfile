FROM python:3.12.5

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

CMD ["python", "-m", "src.live.prepare_dashboard"]