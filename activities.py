from dataclasses import dataclass
from temporalio import activity
import aiohttp

@dataclass
class HttpRequestParams:
    method: str
    url: str
    params: dict = None
    headers: dict = None
    data: dict = None

@activity.defn(name="http_request_activity")
async def http_request_activity(input: HttpRequestParams) -> str:
    async with aiohttp.ClientSession() as session:
        if input.method == 'GET':
            async with session.get(input.url, params=input.params, headers=input.headers) as response:
                return await response.text()
        elif input.method == 'POST':
            async with session.post(input.url, params=input.params, headers=input.headers, json=input.data) as response:
                return await response.text()
        else:
            return "Unsupported HTTP method"