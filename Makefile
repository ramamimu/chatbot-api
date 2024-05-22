init:
	docker compose -f ./compose/postgres.yaml up -d
	docker exec -ti postgres_chatbot psql -U postgres -c "CREATE DATABASE chatbot"

migrate-up:
	alembic upgrade +1

migrate-down:
	alembic downgrade -1

migrate-commit:
	@if [ -z "$(m)" ]; then \
		echo "Commit message is required. Usage: make migratecommit m=\"your message\""; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(m)"

migrate-history:
	alembic history

migrate-checkout:
	@if [ -z "$(r)" ]; then \
		echo "Revision ID is required. Usage: make migrate-checkout r=<revision-id>"; \
		exit 1; \
	fi
	alembic upgrade $(r)

db-up:
	docker compose -f ./compose/postgres.yaml up -d

db-down:
	docker compose -f ./compose/postgres.yaml up -d

start:
	docker compose up -d