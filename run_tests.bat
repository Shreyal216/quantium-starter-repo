@echo off
REM CI/CD Test Runner Script for Quantium Dash App
REM This script activates the virtual environment and runs the test suite

echo.
echo ================================
echo Starting Test Suite Execution
echo ================================
echo.

REM Step 1: Activate virtual environment
echo Step 1: Activating virtual environment...

if not exist "venv" (
    echo Error: Virtual environment not found!
    exit /b 1
)

call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Step 2: Run tests
echo Step 2: Running test suite with pytest...
echo.

pytest test_app.py -v

set TEST_RESULT=%errorlevel%

echo.
echo ================================

if %TEST_RESULT% equ 0 (
    echo [OK] All tests passed successfully!
    echo ================================
    exit /b 0
) else (
    echo [FAIL] Tests failed!
    echo ================================
    exit /b 1
)