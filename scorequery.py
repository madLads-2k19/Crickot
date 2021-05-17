from setInterval import setInterval
from bs4 import BeautifulSoup
import requests
import asyncio

intervalTime = 5

class ScoreQuery:

    def __init__(self, url, intervalTime, channel, eventLoop):
        self.url = url
        self.repeater = setInterval(intervalTime, self.get_score)
        self.channel = channel
        self.eventLoop = eventLoop
        print("Timer set")
    
    def get_score(self):
        page = requests.get(self.url)

        soup = BeautifulSoup(page.content, 'html.parser')

        match = soup.find_all('div', class_ = 'match-header')
        match = match[0]

        team_names = match.find_all('p', class_ = 'name')
        scores = match.find_all('span', class_ = 'score')

        scoreString = '```'
        for (team_name, score) in zip(team_names, scores):
            print(team_name.text, ":", score.text)
            scoreString += (team_name.text + ":" + score.text + "\n")
        scoreString += '```'
        
        sendReply = asyncio.run_coroutine_threadsafe(self.channel.send(scoreString), self.eventLoop)
        sendReply.result()

    def clear(self):
        print("Timer cleared")
        self.repeater.cancel()