FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root


ENV PATH="/app/.venv/bin:$PATH"


EXPOSE 8000

COPY main.py .
COPY kalshi/ ./kalshi/
COPY polymarket/ ./polymarket/
COPY tools/ ./tools/

CMD ["python", "main.py"]
