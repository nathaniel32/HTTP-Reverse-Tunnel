@echo off
set PYTHON_CMD=python
set PYTHON_ARGS=-m
set SCRIPT_PATH=worker.main
set RESTART_DELAY=5

:loop
echo Running %PYTHON_CMD% %PYTHON_ARGS% %SCRIPT_PATH% %*
%PYTHON_CMD% %PYTHON_ARGS% %SCRIPT_PATH% %*

echo %SCRIPT_PATH% crashed. Restarting in %RESTART_DELAY% seconds...
timeout /t %RESTART_DELAY% /nobreak >nul
goto loop