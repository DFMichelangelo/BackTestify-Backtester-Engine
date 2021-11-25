import json
global configuration
configuration = None
with open('./configuration.json') as config_file:
    configuration = json.load(config_file)
