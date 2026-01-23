from pydantic import BaseModel
from typing import Optional

class WorkerConfig(BaseModel):
    proxy_server_url: str
    target_hostname: str
    reconnect_delay: int
    request_timeout: float
    chunk_size: int
    api_key: Optional[str]


import argparse
parser = argparse.ArgumentParser(description="Worker")
parser.add_argument("--server-url", type=str)
parser.add_argument("--target-hostname", type=str)
parser.add_argument("--server-api-key", type=str)
args = parser.parse_args()

worker_config = WorkerConfig(
    proxy_server_url="ws://localhost:8080/worker",
    target_hostname=args.target_hostname,
    reconnect_delay=5,      # Delay in seconds before reconnecting
    request_timeout=30.0,   # Request timeout in seconds
    chunk_size=65536,
    api_key=None            # server api key
)

if args.server_url:
    worker_config.proxy_server_url = args.server_url
if args.server_api_key:
    worker_config.api_key = args.server_api_key