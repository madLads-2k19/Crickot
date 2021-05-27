class Bowler:

    def __init__(self, trow):
        cols = trow.find_all("td")
        playerText = cols[0].find("a", class_ = "player-name").text
        if '(' in playerText:
            self.playerName = playerText[ : playerText.index('(')]
        else:
            self.playerName = playerText
        
        self.overs_bowled = cols[1].text
        self.runs = cols[3].text
        self.wickets = cols[4].text

    def __str__(self):
        return f"{self.playerName} {self.wickets} - {self.runs} ({self.overs_bowled})"
    
    def __repr__(self):
        return str(self)
