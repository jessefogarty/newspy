import asyncio
import aiohttp

async def download(url:str, session: aiohttp.ClientSession) -> tuple[str, str]:
    '''
    Download a url

    Args:
        url (str): The url to download
        session (aiohttp.ClientSession): The session to use
    Returns:
        tuple[str, str]: The url and the html
    '''
    async def _get_html(url:str, session) -> str:
        '''
        Get the html from a url
        '''
        async with session.get(url) as response:
            return await response.text()

    return url, await _get_html(url, session)