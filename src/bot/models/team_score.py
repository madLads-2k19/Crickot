class TeamScore:

    @staticmethod
    def multipleScores(teamScoreHtml):
        score = teamScoreHtml.find('span', class_='score').text
        if '&' in score:
            return True
        return False

    def __init__(self, teamScoreHtml, scoreNum=False):
        self.validScore = False
        # print(teamScoreHtml)
        if teamScoreHtml:
            self.validScore = True
            self.oversData = teamScoreHtml.find('span', class_='score-info').text
            # print(teamScoreHtml.find('span', class_ = 'score'))
            score = teamScoreHtml.find('span', class_='score').text
            # print("Handling score: ", score)
            if scoreNum:
                scoreNum -= 1
                score = score.split('&')[scoreNum]

            if '/' in score:
                [self.runs, self.wickets] = score.split('/')
            else:
                self.runs = score
                self.wickets = 10

    def __bool__(self):
        return self.validScore

    def short_str_repr(self):
        if self.validScore:
            if self.wickets == 10:
                return f"{self.runs} all out"
            return f"{self.runs}/{self.wickets}"

    def long_str_repr(self):
        if self.validScore:
            if self.wickets == 10:
                return f"{self.runs} all out {self.oversData}"
            return f"{self.runs}/{self.wickets} {self.oversData}"

    def __str__(self):
        return self.long_str_repr()
    
    def __repr__(self):
        return str(self)