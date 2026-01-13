start cmd /k uvicorn server.main:app --host 0.0.0.0 --port 8080
TIMEOUT /t 3
start cmd /k python -m worker.main
TIMEOUT /t 3
start cmd /k node test/test_ollama.js