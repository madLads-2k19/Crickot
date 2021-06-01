# A dictionary whose keys are predicate functions and values are functions that return the embed field

from src.config import Settings
import inspect
SETTINGS = Settings.get_settings()

class Predicates:
    batterPredicateDict = {}
    bowlerPredicateDict = {}

    @classmethod
    def load_predicates(cls):
        wicketPredicate = lambda batter: batter.dismissed

        wicketPredicateEmbedField = lambda batter: {"name": "Wicket!", "value": f"{str(batter)}"}

        cls.batterPredicateDict[wicketPredicate] = wicketPredicateEmbedField

        cls.load_batter_run_milestones()
        cls.load_bowler_wicket_milestones()
    
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


    @staticmethod
    def get_bowler_lambda(milestoneWickets):
        return lambda bowler: int(bowler.wickets) > milestoneWickets
    
    @staticmethod
    def get_bowler_embed(milestoneWickets):
        return lambda bowler: {"name": f"{milestoneWickets} - fer!", "value": f"{milestoneRuns} wickets for {bowler.name}"}

    @classmethod
    def load_bowler_wicket_milestones(cls):
        milestoneList = SETTINGS["bowlerWicketMilestones"]

        for milestone in milestoneList:
            milestonePredicate = cls.get_bowler_lambda(milestone)
            milestoneEmbedField = cls.get_bowler_embed(milestone)

            cls.bowlerPredicateDict[milestonePredicate] = milestoneEmbedField

