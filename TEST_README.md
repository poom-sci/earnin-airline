# Integration Tests

> **Note:** This guide is written for macOS. Docker Desktop for Mac is required.

This folder contains integration tests for the EarnIn Airline API, covering passenger booking, updates, deletions, and flight retrieval with timezone conversions.

## Table of Contents

- [Test Coverage](#test-coverage)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [Test Results & Reports](#test-results--reports)
  - [Terminal Output](#terminal-output)
  - [HTML Report](#html-report)
  - [GitHub Actions](#github-actions)
- [Important Notes](#important-notes)

---

## Test Coverage

| Test Category | Description |
|--------------|-------------|
| **Create Booking** | Valid bookings and name validation errors |
| **Update Passenger** | Customer information updates with validation |
| **Delete Passenger** | Booking deletion functionality |
| **Retrieve Flight** | Timezone conversion (same & different timezones) |

---

## Quick Start

### 1. Setup Environment

**Option A: Using Makefile (Recommended)**
```bash
make setup
```

**Option B: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Start Docker services
docker compose up -d
docker compose exec postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

### 2. Run Tests

```bash
make test
# or
pytest
```

---

## Running Tests

### Basic Commands

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `pytest` | Run all tests (alternative) |
| `pytest -v` | Verbose output |
| `pytest -vv` | Extra verbose output |
| `pytest -s` | Show print statements |

### Run Specific Tests

```bash
# Specific file
pytest tests/create_booking_test.py

# Specific class
pytest tests/create_booking_test.py::TestCreateBooking

# Specific test method
pytest tests/create_booking_test.py::TestCreateBooking::test_create_booking_with_valid_customer_and_flight_details
```

### Using Makefile

```bash
make test          # Run all tests
make test-v        # Verbose mode
make test-vv       # Extra verbose mode
make test-s        # Show print statements
make test-report   # Generate HTML report
make test-file     # Interactive: select specific file
```

---

## Test Results & Reports

### Terminal Output

After running tests, you'll see:

```
tests/create_booking_test.py::TestCreateBooking::test_create_booking_with_valid_customer_and_flight_details PASSED [12%]
tests/create_booking_test.py::TestCreateBooking::test_create_booking_with_mismatched_customer_name PASSED [25%]
tests/update_passenger_test.py::TestUpdatePassenger::test_update_customer_information_and_flight_details PASSED [37%]
...

============================= 8 passed in 2.34s =============================
```

**Legend:**
- ✅ `PASSED` - Test succeeded
- ❌ `FAILED` - Test failed (with error details)
- ⏩ `SKIPPED` - Test skipped

---

### HTML Report

Generate a detailed HTML report with test results:

```bash
make test-report
```

This creates `test_report.html` with:
- ✅ Test execution summary
- 📊 Pass/fail statistics
- ⏱️ Execution time for each test
- 🔍 Detailed error messages and stack traces

**Requirements:** `pytest-html` (included in `requirements.txt`)

**View Report:**
```bash
open test_report.html
```

---

### GitHub Actions

**Automated Testing:** Tests run automatically on every push and pull request.

**View Results:**
1. Navigate to [Actions tab](https://github.com/poom-sci/earnin-airline/actions)
2. Select workflow run (e.g., "Deploy Test CI")
3. Check "Run tests" step for output

**Workflow File:** `.github/workflows/deploy-test-ci.yml`

**Features:**
- 🐳 Automatic Docker service setup (PostgreSQL + Wiremock)
- 📦 Dependency installation
- 🗄️ Database schema initialization
- ✅ Full test suite execution
- 📝 Test results in workflow logs

---

## Important Notes

⚠️ **Prerequisites:**
- Docker Desktop for Mac must be running before executing tests
- PostgreSQL runs on port `5432`
- Wiremock runs on port `8081`

📝 **Test Behavior:**
- Tests use shared PostgreSQL database from Docker Compose
- Wiremock mocks the Passport API
- Test data is automatically cleaned up after each test
- Each test file has its own `TEST_FLIGHT_ID` constant

🧹 **Cleanup:**
```bash
make clean              # Remove test cache and artifacts
make docker-down        # Stop Docker services
```

🔧 **Troubleshooting:**
- If tests fail, ensure Docker services are running: `docker compose ps`
- Reset database: `make docker-restart`
- View logs: `docker compose logs postgres`
