# A dictionary whose keys are predicate functions and values are functions that return the embed field

from src.config import Settings
import inspect
SETTINGS = Settings.get_settings()

class Predicates:
    batterPredicateDict = {}

    @classmethod
    def load_predicates(cls):
        wicketPredicate = lambda batter: batter.dismissed

        wicketPredicateEmbedField = lambda batter: {"name": "Wicket!", "value": f"{str(batter)}"}

        cls.batterPredicateDict[wicketPredicate] = wicketPredicateEmbedField

        cls.load_batter_run_milestones()
    
    @classmethod
    def get_predicates(cls):
        if not cls.batterPredicateDict:
            cls.load_predicates()
        return cls.batterPredicateDict
    

    @staticmethod
    def get_batter_lambda(milestoneRuns):
        return lambda batter: int(batter.runs) > milestoneRuns
    
    @staticmethod
    def get_batter_embed(milestoneRuns):
        return lambda batter: {"name": f"{milestoneRuns}!", "value": f"{milestoneRuns} up for {batter.name}"}

    @classmethod
    def load_batter_run_milestones(cls):
        milestoneList = SETTINGS["batterRunMilestones"]

        for milestone in milestoneList:
            milestonePredicate = cls.get_batter_lambda(milestone)
            milestoneEmbedField = cls.get_batter_embed(milestone)

            cls.batterPredicateDict[milestonePredicate] = milestoneEmbedField

# class TestBatter:

#     def __init__(self, runs):
#         self.runs = runs

# def main():
#     batPredicates = Predicates.get_predicates()
#     for predicate in batPredicates.keys():
#         print(predicate(TestBatter(9)))
#         print(predicate(TestBatter(19)))
#         print(predicate(TestBatter(29)))



    # TODO
    # @classmethod
    # def load_bowler_wicket_milestones(cls):
    #     milestoneList = SETTINGS["bowlerRunMilestones"]

    #     for milestone in milestoneList:
    #         milestonePredicate = lambda batter: batter.runs > milestone
    #         milestoneEmbedField = lambda batter: {"name": f"{milestone}!", "value": f"{milestone} up for {batter.name}"}

    #         batterPredicateDict[milestonePredicate] = milestoneEmbedField

