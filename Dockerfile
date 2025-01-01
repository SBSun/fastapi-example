FROM python:3.12.4

WORKDIR /app

RUN pip install poetry==1.8.5
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]