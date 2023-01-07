import asyncio
import aiohttp

async def download_html(url:str, session: aiohttp.ClientSession) -> str:

    async with session.get(url) as response:
        return await response.text()