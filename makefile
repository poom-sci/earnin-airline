
integration-test:
	pytest

install:
	pip install -r requirements.txt

docker-up:
	docker compose up
	docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"

