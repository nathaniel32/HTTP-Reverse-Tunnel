from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

def stream():
    for i in range(1, 6):
        yield f"Streaming data {i}\n"
        time.sleep(1)

@app.get("/")
def stream_endpoint():
    return StreamingResponse(stream(), media_type="text/plain")