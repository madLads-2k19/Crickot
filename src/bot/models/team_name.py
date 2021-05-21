class TeamName:
    def __init__(self, teamNameHtml):
        self.name = teamNameHtml.find("p", class_='name').text
        self.batting = None
        self.won = None
        if teamNameHtml.find("span", class_="batting-indicator"):
            self.batting = True
        if teamNameHtml.find("i", class_ = "winner-icon"):
            self.won = True
    
    def get_abbr(self):
        if ' ' in self.name:
            abbr = ''
            for word in self.name.split(' '):
                abbr += word[0]
        else:
            abbr = self.name[:3].upper()

        if self.batting:
            return f"__{abbr}__"
        return abbr
