from src.bot.update.predicates import Predicates
from collections import deque
import inspect

class UpdateManager:

    def __init__(self, url, initialScorecard):
        self.url = url
        self.prevcard = initialScorecard
        self.update_queue = deque([None] * 5, 5)

    def get_update_fields(self, newcard):
        batterPredicateDict = Predicates.get_predicates()

        for predicate in batterPredicateDict.keys():
            prevFiltered = list(filter(predicate, self.prevcard.batters))
            newFiltered = list(filter(predicate, newcard.batters))

            if len(prevFiltered) == len(newFiltered):
                continue
            
            if len(prevFiltered) > len(newFiltered):
                raise Exception("Possible scorecard reset?")
            
            print("UPDATE")

            newBatters = [ batter for batter in newFiltered if batter not in prevFiltered ]
            print(f"NEWBATTERS: f{newBatters}")

            for newBatter in newBatters:
                updateEmbed = batterPredicateDict[predicate](newBatter)
                self.update_queue.appendleft(updateEmbed)
        
        print(self.update_queue)
        
        updateFields = [ field for field in list(self.update_queue) if field != None ]
        print(f"UPDATE FIELDS: {updateFields}")
        self.prevcard = newcard
        return updateFields

