.PHONY: run dev test lint fmt migrate-up migrate-rev alembic-init


run:
uvicorn app.main:app --host 0.0.0.0 --port 8000


dev:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


test:
pytest -q --cov=app --cov-report=term-missing


lint:
ruff check app


fmt:
ruff format app


alembic-init:
alembic init -t async migrations


migrate-rev:
alembic revision --autogenerate -m "auto"


migrate-up:
alembic upgrade head