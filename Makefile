init:
	docker compose -f ./compose/postgres.yaml up -d
	docker exec -ti postgres_chatbot psql -U postgres -c "CREATE DATABASE chatbot"

drop-table-files:
	docker exec -ti postgres_chatbot psql -U postgres -d chatbot -c "DROP TABLE files"

drop-alembic-db:
	docker exec -ti postgres_chatbot psql -U postgres -d chatbot -c "DROP TABLE alembic_version;"

reset-files-table:
	docker exec -ti postgres_chatbot psql -U postgres -d chatbot -c "TRUNCATE TABLE files; DROP SEQUENCE files_id_seq;"

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

docker-start:
	docker compose up -d

start:
	python3 app.py

start-test:
	alembic upgrade head
	python3 app.py test

start-deploy:
	fastapi run app.py