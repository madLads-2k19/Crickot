class Batter:

    def __init__(self, trow):
        cols = trow.find_all("td")
        playerText = cols[0].find("a", class_ = "player-name").text
        if '(' in playerText:
            self.playerName = playerText[ : playerText.index('(')]
        else:
            self.playerName = playerText
        
        self.runs = cols[1].text
        self.balls_faced = cols[2].text

    def __str__(self):
        return f"{self.playerName} {self.runs} ({self.balls_faced})"
    
    def __repr__(self):
        return str(self)
