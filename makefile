
.PHONY: install docker-up docker-down setup test test-v test-vv test-s test-report test-file clean

install:
	pip install -r requirements.txt

docker-up:
	docker compose up -d
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	docker compose exec postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
	@echo "Docker services are up and schema initialized!"

docker-down:
	docker compose down

setup: install docker-up
	@echo "Setup complete! Run 'make test' to run tests."

test:
	pytest

test-report:
	pytest --html=test_report.html --self-contained-html -sv
	@echo "Test report generated: test_report.html"

test-v:
	pytest -v

test-vv:
	pytest -vv

test-s:
	pytest -s

test-file:
	@read -p "Enter test file (e.g., tests/create_booking_test.py): " file; \
	pytest $$file -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f test_report.html
	@echo "Cleaned up test cache and Python artifacts"

