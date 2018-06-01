import time
import yaml
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

BOTUPTIME = time.time()

status = ["Paying what you want.",
          "Supporting charity.",
          "Getting awesome games."]

with open("rss.yml", 'r') as file_rss:
    RSSYAML = yaml.load(file_rss)