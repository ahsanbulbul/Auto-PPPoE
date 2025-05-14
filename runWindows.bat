@echo off
:: filepath: /Projects/Auto-PPPoE/runWindows.bat
setlocal

:: Set application location
set APP_LOCATION=C:\path\to\Auto-PPPoE
set LOG_FILE=%APP_LOCATION%\pppoe_automation.log

:: Add timestamp for start of execution
echo %date% %time% [Start] >> "%LOG_FILE%"
echo ====================================================== >> "%LOG_FILE%"

:: Change to project directory
cd /d "%APP_LOCATION%"

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Run the automation script and capture all output
python "%APP_LOCATION%\PPPoE_Automation.py" %* >> "%LOG_FILE%" 2>&1

:: Add timestamp for end of execution
echo ====================================================== >> "%LOG_FILE%"
echo %date% %time% [Stop] >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

:: Deactivate the virtual environment
call deactivate

endlocal