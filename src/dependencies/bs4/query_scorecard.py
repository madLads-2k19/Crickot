from bs4 import BeautifulSoup
import aiohttp
import os

class QueryScorecard:
    @staticmethod
    async def query_latest_scorecard(scorecardUrl):
        url = os.getenv("MAIN_URL") + scorecardUrl
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                matchHeader = soup.find("div", class_ = "match-header")
                scorecards = soup.find_all("div", class_ = "match-scorecard-table")
                latest_scorecard = scorecards[-2]
                return matchHeader, latest_scorecard
