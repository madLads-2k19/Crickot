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
        print("Initialized wicket update")
        self.prevWickets, self.prevDismissedBatters = WicketUpdate.getWicketDetails(initialScorecard)
        print(self.prevWickets, self.prevDismissedBatters, sep = "\n")
    
    def get_embed_fields(self, newScorecard):
        print("Get embed fields called")
        newWickets, newDismissedBatters = WicketUpdate.getWicketDetails(newScorecard)
        print(newWickets)
        print(newDismissedBatters)
        if newWickets == self.prevWickets:
            return None
        dismissedBattersDiff = list(set(newDismissedBatters) - set(self.prevDismissedBatters))
        
        fieldList = []
        for batter in dismissedBattersDiff:
            embedFieldDict = {"name": "Wicket!", "value": f"{str(batter)}"}
            fieldList.append(embedFieldDict)

        print(fieldList)
        return fieldList

    # def get_embed_fields(self, newScorecard):
    #     dummyFieldList = [
    #         {
    #             "name": "Dummy field",
    #             "value": "Dummy value"
    #         },
    #         {
    #             "name": "Another dummy field",
    #             "value": "I am bored"
    #         }
    #     ]
    #     print("Get embed field called")
    #     return dummyFieldList