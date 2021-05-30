from src.bot.update.wicket_update import WicketUpdate

class UpdateManager:

    def __init__(self, url, initialScorecard):
        self.url = url
        self.wktupdate = WicketUpdate(initialScorecard)
    
    def get_update_fields(self, newScorecard):
        return self.wktupdate.get_embed_fields(newScorecard)