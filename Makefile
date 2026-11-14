.PHONY: setup dev test lint migrate seed e2e format

setup:
	cd backend && pip install -e ".[dev]"
	cd frontend && pnpm install
	cp -n .env.example .env || true
	cd backend && alembic upgrade head

dev:
	start cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"
	cd frontend && pnpm dev

test:
	cd backend && pytest tests/ -v
	cd frontend && pnpm test

lint:
	cd backend && ruff check app/ tests/
	cd backend && mypy app/
	cd frontend && pnpm lint

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python scripts/seed.py

e2e:
	cd e2e && npx playwright test

format:
	cd backend && ruff format app/ tests/
	cd frontend && pnpm prettier --write src/
