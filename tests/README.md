1. Start docker first:
```bash
docker compose up -d
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

2. Install test packages:
```bash
pip install -r requirements.txt
```

3. Run test:
```bash
pytest
```

or run specific test file:
```bash
pytest tests/create_booking_test.py
```
