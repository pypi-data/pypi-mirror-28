"""card-py-bot

A Discord.py bot server that allows for user typed links of Magic cards (based
off of the http://gatherer.wizards.com/Pages/Card Magic card info repository)
to be automatically embedded into the discord chat. The embedded message
created by the card-py-bot details basic details of the Magic card, as well
as the cards image itself.

Scripts:
    __main__

Modules:
    bot
    config
    scrape

Config:
    emoji_config.json
"""

import os

BASEDIR = os.path.dirname(os.path.realpath(__file__))

WIZARDS_BASE_URL = "http://gatherer.wizards.com/"
