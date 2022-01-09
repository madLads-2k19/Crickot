from bs4 import BeautifulSoup
import aiohttp
import os

class QueryLiveMatch:
    @staticmethod
    async def query_live_match(matchUrl):
        # url = 'https://www.espncricinfo.com/series/ireland-inter-provincial-limited-over-cup-2021-1259520/munster-reds-vs-northern-knights-10th-match-1259532/live-cricket-score'
        url = os.getenv("MAIN_URL") + matchUrl
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                matchHeader = soup.find("div", class_ = "match-header")
                liveScorecard = soup.find("div", class_ = "live-scorecard")
                return matchHeader, liveScorecard

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    import asyncio

    asyncio.get_event_loop().run_until_complete(QueryCricketData().query_live_matches())