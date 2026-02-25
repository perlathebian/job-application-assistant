import httpx

import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


async def call_api(endpoint: str, method: str = "POST", **kwargs):
    """Make async API call"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "POST":
            response = await client.post(url, **kwargs)
        elif method == "GET":
            response = await client.get(url, **kwargs)
        elif method == "DELETE":
            response = await client.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
        response.raise_for_status()
        return response.json()