from src.bot.models.team_score import TeamScore
from src.bot.models.team_name import TeamName
from src.bot.models.batter import Batter
from src.bot.models.bowler import Bowler

class LiveMatchData:

    def __init__(self, matchHeader, liveScorecard):

        teamsData = matchHeader.find_all('div', class_='team')

        [self.team1, self.team2] = [TeamName(data) for data in teamsData]

        self.team1Scores = []
        self.team2Scores = []

        teamScoreDataHtml1 = teamsData[0].find('div', class_='score-detail')
        if teamScoreDataHtml1:
            if TeamScore.multipleScores(teamScoreDataHtml1):
                self.team1Scores.append(TeamScore(teamScoreDataHtml1, 1))
                self.team1Scores.append(TeamScore(teamScoreDataHtml1, 2))
            else:
                self.team1Scores.append(TeamScore(teamScoreDataHtml1))
        
        teamScoreDataHtml2 = teamsData[1].find('div', class_='score-detail')
        if teamScoreDataHtml2:
            if TeamScore.multipleScores(teamScoreDataHtml2):
                self.team2Scores.append(TeamScore(teamScoreDataHtml2, 1))
                self.team2Scores.append(TeamScore(teamScoreDataHtml2, 2))
            else:
                self.team2Scores.append(TeamScore(teamScoreDataHtml2))
        

        scoreTable = liveScorecard.find("table")
        [batData, bowlData] = scoreTable.find_all("tbody")

        self.batters = []
        self.bowlers = []

        for row in batData.find_all("tr"):
            self.batters.append(Batter(row))
        
        for row in bowlData.find_all("tr"):
            self.bowlers.append(Bowler(row))
        
        print(self.team1, self.team2)
        print(self.team1Scores, self.team2Scores, sep = "\n")
        print(self.batters, self.bowlers, sep = "\n")

    def get_embed(self):
        scoreValue = "Nothing here yet"
        if self.team1Scores:
            if len(self.team1Scores) == 2:
                scoreValue = f"{self.team1}: {self.team1Scores[0] & self.team1Scores[1]}"
            if len(self.team1Scores) == 1:
                scoreValue = f"{self.team1}: {self.team1Scores[0]}"
        
        if self.team2Scores:
            if len(self.team2Scores) == 2:
                scoreValue += f"\n{self.team2}: {self.team2Scores[0] & self.team2Scores[1]}"
            if len(self.team2Scores) == 1:
                scoreValue += f"\n{self.team2}: {self.team2Scores[0]}"
            
        batterValue = ""
        for batter in self.batters:
            batterValue += str(batter) + "\n"
        
        bowlerValue = ""
        for bowler in self.bowlers:
            bowlerValue += str(bowler) + "\n"

        embed = {
            "title": f"{self.team1}   :vs:   {self.team2}",
            # "description": "The Live Cricket Matches happening around the world!",
            "fields": [
                {
                    "name": "Live Score",
                    "value": scoreValue,
                    "inline": False
                },
                {
                    "name": "Batting",
                    "value": batterValue,
                    "inline": True
                },
                {
                    "name": "Bowling",
                    "value": bowlerValue,
                    "inline": True
                }
            ],
            "color": 65484,
            "provider": {"name": "ESPNCricinfo", "url": "https://www.espncricinfo.com"},
        }
        return embed