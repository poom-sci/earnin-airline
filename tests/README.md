# Integration Tests

This folder contains integration tests for the EarnIn Airline API, covering passenger booking, updates, deletions, and flight retrieval with timezone conversions.

## Test Coverage

- **Create Booking**: Valid bookings and mismatch name validation
- **Update Passenger**: Customer information updates and validation
- **Delete Passenger**: Booking deletion
- **Retrieve Flight**: Timezone conversion for different and same timezones

## How to Run Tests

### Prerequisites

1. **Start Docker services** (PostgreSQL + Wiremock):
```bash
docker compose up -d
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

or using makefile:
```bash
make compose-up
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/create_booking_test.py
```

**Run with verbose output:**
```bash
pytest -v
```

**Run with print statements visible:**
```bash
pytest -s
```

**Run specific test class:**
```bash
pytest tests/create_booking_test.py::TestCreateBooking -s
```

**Run with detailed output:**
```bash
pytest -vv
```

## Test Results & Reports

### Local Test Results

After running `pytest`, results are displayed in the terminal with:
- ✓ **Green dots** - Passed tests
- ✗ **Red F** - Failed tests  
- Test execution time
- Summary of passed/failed/skipped tests

**Example output:**
```
tests/create_booking_test.py::TestCreateBooking::test_create_booking_with_valid_customer_and_flight_details PASSED
tests/create_booking_test.py::TestCreateBooking::test_create_booking_with_mismatched_customer_name PASSED
============================= 2 passed in 1.23s =============================
```

### GitHub Actions

Tests run automatically on:
- Every push to any branch
- Every pull request to `main`

**View test results:**
1. Go to repository **[Actions tab](https://github.com/poom-sci/earnin-airline/actions)**
2. Click on the workflow run (e.g., "Deploy Test CI")
3. View test execution logs under "Run tests" step

**Direct workflow file:** `.github/workflows/deploy-test-ci.yml`

### Test Reports (Optional)

To generate HTML test report:
```bash
pytest --html=report.html --self-contained-html
```

View `report.html` in browser for detailed test results with timestamps and failure details.

## Notes

- Tests use shared PostgreSQL database from Docker Compose
- Wiremock runs on port 8081 for Passport API mocking
- Test data is automatically cleaned up after each test
- Make sure Docker services are running before executing tests
- Each test file has its own `TEST_FLIGHT_ID` constant for readability
