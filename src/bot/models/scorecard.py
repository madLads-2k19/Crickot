from src.bot.models.scorecard_batter import ScorecardBatter
from src.bot.models.scorecard_bowler import ScorecardBowler
from src.bot.models.team_name import TeamName
from src.bot.models.team_score import TeamScore

class Scorecard:
    def __init__(self, matchHeader, scorecardHtml):

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

        
        batsmanTable = scorecardHtml.find("table", class_ = "batsman")
        batsmanTableBody = batsmanTable.find("tbody")
        
        batsmanTableRows = batsmanTableBody.find_all("tr")[:-1]
        batsmanTableRows = batsmanTableRows[::2]

        print("\nBatters:\n")

        self.batters = [ScorecardBatter(row) for row in batsmanTableRows]

        bowlerTable = scorecardHtml.find("table", class_ = "bowler")
        bowlerTableBody = bowlerTable.find("tbody")
        
        bowlerTableRows = bowlerTableBody.find_all("tr")

        print("\nBowlers:\n")

        self.bowlers = [ScorecardBowler(row) for row in bowlerTableRows]
    


