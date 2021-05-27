import json

class Settings:
    settings = None

    @classmethod
    def load_settings(cls):
        f = open('settings.json')
        cls.settings = json.load(f)

    @classmethod
    def get_settings(cls):
        if not cls.settings:
            cls.load_settings()
        return cls.settings