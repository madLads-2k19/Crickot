from src.bot.models.team_score import TeamScore
from src.bot.models.team_name import TeamName


class LiveMatchOverview:
    def __init__(self, cardHtml):
        self.url = cardHtml.find('a', class_="match-info-link-HSB")["href"]
        matchInfoHtml = cardHtml.find('div', class_="match-info")
        statusData = matchInfoHtml.find('div', class_="status")

        status = statusData.find("span", class_=None).text
        if "(" in status:
            bracketIndex = status.index("(")
            status = status[:bracketIndex]
        self.status = status.title()

        descriptionData = statusData.find('span', class_="hsb-description").text.split("\N{BULLET}")
        # print(descriptionData)
        if descriptionData:
            # print(descriptionData)
            if len(descriptionData) == 3:
                [_, matchType, location] = descriptionData
            if len(descriptionData) == 2:
                [_, location] =  descriptionData
                matchType = "Unknown"

        self.matchType = matchType.strip()
        self.location = location.strip()

        teamsData = matchInfoHtml.find_all('div', class_='team')

        [self.team1, self.team2] = [TeamName(data) for data in teamsData]

        [self.team1score, self.team2score] = [TeamScore(teamData.find('div', class_='score-detail')) for teamData in
                                              teamsData]

        self.footer = matchInfoHtml.find('div', class_='status-text').find('span').text

    def get_embed_field(self):
        name = f"{self.team1.get_abbr()}   :vs:   {self.team2.get_abbr()}"

        if self.team1.batting:
            value = self.team1score.long_str_repr()
        elif self.team2.batting:
            value = self.team2score.long_str_repr()
        else:
            if self.team1.won:
                value = self.team1.get_abbr() + "  :trophy:"
            elif self.team2.won:
                value = self.team2.get_abbr() + "  :trophy:"
            else:
                value = self.status

        value += "\n" + self.location

        if "Rain" in self.status:
            value += "  :cloud_rain:"
        if "Light" in self.status:
            value += "  :cloud:"

        name = "\t\t" + name
        value = "\t\t" + value
        return {'name': name, 'value': value, 'inline': True}
