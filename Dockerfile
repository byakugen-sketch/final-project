FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
RUN pip uninstall -y setuptools wheel
COPY app.py .
COPY static/ ./static/
COPY tests/ ./tests/
EXPOSE 5000
CMD ["python", "app.py"]