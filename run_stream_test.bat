start run.bat
TIMEOUT /t 3
start cmd /k "cd /d %~dp0\test && set SERVER_NAME=Server 1 && uvicorn test_stream:app --port 20001"
start cmd /k python -m worker.main --target-hostname http://localhost:20001

start cmd /k "cd /d %~dp0\test && set SERVER_NAME=Server 2 && uvicorn test_stream:app --port 20002"
start cmd /k python -m worker.main --target-hostname http://localhost:20002