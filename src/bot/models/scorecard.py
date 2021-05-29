from src.bot.models.scorecard_batter import ScorecardBatter
# from scorecard_bowler import ScorecardBowler

class Scorecard:
    def __init__(self, scorecardHtml):
        batsmanTable = scorecardHtml.find("table", class_ = "batsman")
        batsmanTableBody = batsmanTable.find("tbody")
        
        batsmanTableRows = batsmanTableBody.find_all("tr")[:-1]
        batsmanTableRows = batsmanTableRows[::2]

        self.batters = [ScorecardBatter(row) for row in batsmanTableRows]

        # bowlerTable = scorecardHtml.find("table", class_ = "bowler")
        # bowlerTableBody = bowlerTable.find("tbody")
        
        # bowlerTableRows = bowlerTableBody.find("tr")

        # self.bowlers = [ScorecardBowler(row) for row in bowlerTableRows]
    


