include .env

migration:
	goose -dir db/migrations create $(name) sql

migratedb:
	goose -dir 'db/migrations' postgres ${DATABASE_URL} up

rollback:
	goose -dir 'db/migrations' postgres ${DATABASE_URL} down

up:
	docker compose build
	docker-compose up --remove-orphans -d
ps:
	docker-compose ps

down:
	docker-compose down --remove-orphans

logs:
	docker-compose logs -f

stop:
	docker-compose stop --remove-orphans

populate:
	python db/scripts/data_cleaning.py

convert:
	python app/utils/currency_converter.py

test:
	pytest

celery:
	celery -A run.celery worker --loglevel=info

beat:
	celery -A run.celery beat -S redbeat.RedBeatScheduler --max-interval 30 --loglevel=info

server:
	FLASK_APP=run.py flask run -h 0.0.0.0 -p 5080 --reload

analysis:
	python db/scripts/analysis.py