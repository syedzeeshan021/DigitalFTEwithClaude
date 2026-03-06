@echo off
REM AI Employee Bronze Tier Startup Script

echo Starting AI Employee - Bronze Tier Implementation
echo =================================================

echo Setting up environment...
set VAULT_PATH=AI_Employee_Vault

echo Creating required directories if they don't exist...
if not exist "%VAULT_PATH%" mkdir "%VAULT_PATH%"
if not exist "%VAULT_PATH%\Inbox" mkdir "%VAULT_PATH%\Inbox"
if not exist "%VAULT_PATH%\Needs_Action" mkdir "%VAULT_PATH%\Needs_Action"
if not exist "%VAULT_PATH%\Done" mkdir "%VAULT_PATH%\Done"
if not exist "%VAULT_PATH%\Plans" mkdir "%VAULT_PATH%\Plans"
if not exist "%VAULT_PATH%\Logs" mkdir "%VAULT_PATH%\Logs"
if not exist "%VAULT_PATH%\Pending_Approval" mkdir "%VAULT_PATH%\Pending_Approval"
if not exist "%VAULT_PATH%\Approved" mkdir "%VAULT_PATH%\Approved"
if not exist "%VAULT_PATH%\Rejected" mkdir "%VAULT_PATH%\Rejected"

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo To start the AI Employee system:
echo.
echo 1. In one terminal, run: python orchestrator.py
echo 2. In another terminal, run: python filesystem_watcher.py
echo.
echo The system is now ready! Place files in the %VAULT_PATH%\Inbox folder to test.
echo.

pause