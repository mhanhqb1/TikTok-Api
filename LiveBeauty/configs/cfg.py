import os
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
PATH_CONFIG = os.path.join(dir_path, "config.json")
def run():
    with open(PATH_CONFIG) as screeners:
        config = json.loads(screeners.read())
        for key in config.keys():
            os.environ[key] = config[key]