import asyncio
import websockets
import json
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
TARGET_API_HOST = "localhost"
TARGET_API_PORT = 11434
TARGET_API_SCHEME = "http"
TARGET_API_URL = f"{TARGET_API_SCHEME}://{TARGET_API_HOST}:{TARGET_API_PORT}"

PROXY_SERVER_URL = "ws://localhost:8000/worker"

async def handle_request(request_data: dict):
    """Make HTTP request to target API and yield response parts"""
    request_id = request_data["request_id"]
    method = request_data["method"]
    path = request_data["path"]
    headers = request_data.get("headers", {})
    body = request_data.get("body")
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    url = f"{TARGET_API_URL}{path}"
    logger.info(f"Worker processing request {request_id}: {method} {url}")
    
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                method=method,
                url=url,
                headers=headers,
                content=body.encode() if body else None,
                timeout=30.0
            ) as response:
                
                # Send start of response
                yield {
                    "type": "response_start",
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content_type": response.headers.get("content-type", "application/json")
                }
                
                # Stream content
                async for chunk in response.aiter_text():
                    yield {
                        "type": "response_chunk",
                        "request_id": request_id,
                        "chunk": chunk
                    }
                
                # Send end of response
                yield {
                    "type": "response_end",
                    "request_id": request_id
                }
            
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}")
        yield {
            "type": "error",
            "request_id": request_id,
            "error": str(e)
        }

async def worker():
    """Connects to server and processes requests"""
    while True:
        try:
            async with websockets.connect(PROXY_SERVER_URL) as websocket:
                logger.info("Worker connected to proxy server")
                
                async for message in websocket:
                    try:
                        request_data = json.loads(message)
                        
                        if request_data.get("type") == "request":
                            # Process request and send response parts
                            async for response_part in handle_request(request_data):
                                await websocket.send(json.dumps(response_part))
                            
                            logger.info(f"Response sent for request {request_data['request_id']}")
                            
                    except Exception as e:
                        logger.error(f"Error handling message: {e}")
                        
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"WebSocket error: {e}")
            logger.info("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(worker())