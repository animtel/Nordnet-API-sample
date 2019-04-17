import json

SETTINGS_PATH = 'settings.json'
json_string = open(SETTINGS_PATH).read()
settings = json.loads(json_string)
