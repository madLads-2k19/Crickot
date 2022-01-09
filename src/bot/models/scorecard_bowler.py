class ScorecardBowler:

    def __init__(self, bowlerRow):
        bowlerCols = bowlerRow.find_all("td")

        self.name = bowlerCols[0].text

        self.overs_bowled = bowlerCols[1].text

        self.runs = bowlerCols[3].text

        self.wickets = bowlerCols[4].text

        # print(self)

    def __str__(self):
        return f"{self.name} {self.wickets} - {self.runs} ({self.overs_bowled})"
    
    def __repr__(self):
        return str(self)