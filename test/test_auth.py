import asyncio
import websockets

async def test_invalid_auth():
    try:
        async with websockets.connect(
            "ws://localhost:8080/worker",
            additional_headers={"Authorization": "Bearer default_key"}
        ) as ws:
            print("Connected!")
            data = await ws.recv()
            print(f"Received: {data}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket closed: code={e.code}, reason={e.reason}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

asyncio.run(test_invalid_auth())