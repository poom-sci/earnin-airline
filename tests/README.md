# Integration Tests

## How to run

1. Start docker first:
```bash
docker compose up -d
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

or using makefile

```bash
make compose-up
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

or run with log:
```bash
pytest tests/create_booking_test.py -s
```

or run with specfic class:
```bash
pytest tests/create_booking_test.py::TestCreateBookingIntegration -s
```

## GitHub Actions

Tests run automatically on every PR to main branch. Check the "Actions" tab to see results.

## Notes

- Make sure docker is running before test
- Test data will be cleaned up automatically
