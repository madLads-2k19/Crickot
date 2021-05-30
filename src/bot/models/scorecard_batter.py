class ScorecardBatter:

    def __init__(self, batterRow):
        batterCols = batterRow.find_all("td")
        self.name = batterCols[0].text

        self.dismissDetail = batterCols[1].text

        self.dismissed = False if self.dismissDetail == "not out" else True

        self.runs = batterCols[2].text

        self.balls_faced = batterCols[3].text

        # print(self)

    def __str__(self):
        return f"{self.name} {self.dismissDetail} {self.runs} ({self.balls_faced})"

    def __repr__(self):
        return str(self)