from bs4 import BeautifulSoup
import aiohttp
import os

class QueryCricketData:
    @staticmethod
    async def query_live_matches():
        url = os.getenv("MAIN_URL")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                cards = soup.find_all(True, class_ = "scorecard-container")
                return cards

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import asyncio

    asyncio.get_event_loop().run_until_complete(QueryCricketData().query_live_matches())