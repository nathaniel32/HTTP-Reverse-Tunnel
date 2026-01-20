start run.bat
TIMEOUT /t 3
start cmd /k python -m http.server 10001 --directory test/web/1
start cmd /k python -m http.server 10002 --directory test/web/2
start cmd /k python -m worker.main --target-hostname http://localhost:10001/
start cmd /k python -m worker.main --target-hostname http://localhost:10002/