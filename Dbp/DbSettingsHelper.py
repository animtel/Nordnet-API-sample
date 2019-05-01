import json

SETTINGS_PATH = 'DbInitSettings.json'
json_string = open(SETTINGS_PATH).read()
settings = json.loads(json_string)
