class WicketUpdate:

    @staticmethod
    def getWicketDetails(scorecard):
        if scorecard.team2Scores:
            if len(scorecard.team1Scores) == len(scorecard.team2Scores):
                wickets = scorecard.team2Scores[-1].wickets
            else:
                if len(scorecard.team1Scores) > len(scorecard.team2Scores):
                    wickets = scorecard.team1Scores[-1].wickets
                else:
                    wickets = scorecard.team2Scores[-1].wickets
        else:
            wickets = scorecard.team1Scores[0].wickets
            
        dismissedBatters = [batter for batter in scorecard.batters if batter.dismissed]
        
        return wickets, dismissedBatters

    def __init__(self, initialScorecard):
        self.prevWickets, self.prevDismissedBatters = WicketUpdate.getWicketDetails(initialScorecard)
    
    def get_embed_fields(self, newScorecard):
        newWickets, newDismissedBatters = WicketUpdate.getWicketDetails(newScorecard)
        if newWickets == self.prevWickets:
            return None
        dismissedBattersDiff = list(set(newDismissedBatters) - set(self.prevDismissedBatters))
        
        fieldList = []
        for batter in dismissedBattersDiff:
            embedFieldDict = {"name": "Wicket!", "value": f"{str(batter)}"}
            fieldList.append(embedFieldDict)
        
        return fieldList