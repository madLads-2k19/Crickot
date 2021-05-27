class TeamName:
    def __init__(self, teamNameHtml):
        self.name = teamNameHtml.find("p", class_='name').text
        self.batting = None
        self.won = None
        if teamNameHtml.find("span", class_="batting-indicator"):
            self.batting = True
        if teamNameHtml.find("i", class_ = "winner-icon"):
            self.won = True
    
    def get_abbr(self, display : bool = False):
        if ' ' in self.name:
            abbr = ''
            for word in self.name.split(' '):
                abbr += word[0]
        else:
            abbr = self.name[:3].upper()

        if display and self.batting:
            return f"__{abbr}__"
        return abbr

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)