# New Plan
# 
# Define a list of predicates to be applied on each object in a list of batters / bowlers
# For exmample, batter, runs > 50
# 
# Define a class that stores a previous scorecard
# 
# Non boundary condition:
# Input a new scorecard
# Apply filter to old and new scorecard using every predicate
# If the lengths of the outputs are different, use a list comprehension to obtain the difference
# Generate embed fields using the difference

# Append the newly generated embed fields into a queue of fixed mamximum length
# Convert the queue into a list and extend the list to the fields of the existing embed

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
            
            print("Prev filtered")
            print(prevFiltered)
            print("New filtered")
            print(newFiltered)

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
        
        updateFields = [ field for field in list(self.update_queue) if field != None ]
        print(f"UPDATE FIELDS: {updateFields}")
        self.prevcard = newcard
        return updateFields

