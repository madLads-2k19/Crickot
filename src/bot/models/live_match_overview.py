from src.bot.models.team_score import TeamScore
from src.bot.models.team_name import TeamName
from src.config import Settings

SETTINGS = Settings.get_settings()
import datetime
import pytz

class LiveMatchOverview:
    def __init__(self, cardHtml):
        self.url = cardHtml.find('a', class_="match-info-link-HSB")["href"]
        # print("Processed URL: ", self.url)
        matchInfoHtml = cardHtml.find('div', class_="match-info")
        statusData = matchInfoHtml.find('div', class_="status")

        status = statusData.find("span", class_=None).text
        if "(" in status:
            bracketIndex = status.index("(")
            status = status[:bracketIndex]
        
        try:
            matchDateTime = datetime.datetime.strptime(status, SETTINGS["websiteDateTimeFormat"])
            locTime = pytz.utc.localize(matchDateTime).astimezone(pytz.timezone('Asia/Kolkata'))
            self.status = locTime.strftime(SETTINGS["botDateTimeFormat"]) + " IST"

        except ValueError:
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


        self.footer = matchInfoHtml.find('div', class_='status-text').find('span').text

    def get_embed_field(self):
        name = f"{self.team1.get_abbr(display = True)}   :vs:   {self.team2.get_abbr(display = True)}"

        if self.team1.batting:
            value = self.team1Scores[0].long_str_repr()

            if len(self.team1Scores) == 2:
                value += " & " + self.team1Scores[1].long_str_repr()

        elif self.team2.batting:
            value = self.team2Scores[0].long_str_repr()

            if len(self.team2Scores) == 2:
                value += " & " + self.team2Scores[1].long_str_repr()

        else:
            if self.team1.won:
                value = self.team1.get_abbr() + "  :trophy:"
            elif self.team2.won:
                value = self.team2.get_abbr() + "  :trophy:"
            elif self.status == "Result":
                value = self.footer
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

    def is_live(self):
        # print(self.status)
        return  (self.status != "Result" and ":" not in self.status)