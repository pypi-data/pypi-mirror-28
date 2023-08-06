"""Emoji config functions"""
import json
import os
import re
from logging import getLogger

from card_py_bot import BASEDIR

__log__ = getLogger(__name__)

# Path where the emoji_config.json will be stored
EMOJI_CONFIG_PATH = os.path.join(BASEDIR, "emoji_config.json")

# Dictionary that is keyed by the Discord short emoji id and the web id
# of each emoji
MANA_ID_DICT = {
    ":15m:": "15",
    ":13m:": "13",
    ":wbm:": "White or Black",
    ":Energy:": "Energy",
    ":10m:": "10",
    ":7m:": "7",
    ":Untap:": "Untap",
    ":brm:": "Black or Red",
    ":bpm:": "Phyrexian Black",
    ":rgm:": "Red or Green",
    ":9m:": "9",
    ":8m:": "8",
    ":1m:": "1",
    ":gum:": "Green or Blue",
    ":2wm:": "Two or White",
    ":wpm:": "Phyrexian White",
    ":4m:": "4",
    ":12m:": "12",
    ":rm:": "Red",
    ":bm:": "Black",
    ":wum:": "White or Blue",
    ":rwm:": "Red or White",
    ":2bm:": "Two or Blue",
    ":gpm:": "Phyrexian Green",
    ":gm:": "Green",
    ":14m:": "14",
    ":bgm:": "Black or Green",
    ":3m:": "3",
    ":5m:": "5",
    ":Tap:": "Tap",
    ":1000000m:": "1000000",
    ":upm:": "Phyrexian Blue",
    ":2gm:": "Two or Green",
    ":rpm:": "Phyrexian Red",
    ":2m:": "2", ":6m:": "6",
    ":2rm:": "Two or Red",
    ":gwm:": "Green or White",
    ":wm:": "White",
    ":um:": "Blue",
    ":16m:": "16",
    ":urm:": "Blue or Red",
    ":ubm:": "Blue or Black",
    ":11m:": "11"
}


def get_emoji_config_string() -> str:
    """Return a string of all the mana ids (in order) for config setup
    in discord"""
    config_string = "?save_setup\n"
    for short_emoji_id in MANA_ID_DICT:
        config_string += ("\\\\{}\n".format(short_emoji_id))

    return config_string


EMOJI_CONFIG_STRING = get_emoji_config_string()


def create_config_json() -> dict:
    """Create and save a blank default config json also return the dict that
    created the json"""
    emoji_config = dict()

    for short_emoji_id in MANA_ID_DICT:
        emoji_config[short_emoji_id] = {
            "web_id": MANA_ID_DICT[short_emoji_id],
            "discord_raw_id": None
        }

    with open(EMOJI_CONFIG_PATH, "w") as file:
        json.dump(emoji_config, file, indent=4)

    return emoji_config


def load_mana_dict() -> dict:
    """Load the emoji config into a mana dict"""
    try:
        with open(EMOJI_CONFIG_PATH, "r") as file:
            emoji_config = json.load(file)
    except FileNotFoundError:
            emoji_config = create_config_json()

    mana_dict = dict()
    for short_emoji_id in emoji_config:
        emoji = emoji_config[short_emoji_id]
        if not emoji["discord_raw_id"]:
            mana_dict[emoji["web_id"]] = "ERROR: NO ID Configured " \
                                         "for {}".format(emoji["web_id"])
        else:
            mana_dict[emoji["web_id"]] = emoji["discord_raw_id"]

    __log__.debug("WOTC Magic mana to Discord emoji "
                  "dictionary constructed: {}".format(mana_dict))
    return mana_dict


MANA_DICT = load_mana_dict()


def parse_raw_emoji_id(raw_emoji_id: str) -> str:
    """Parse a raw emoji id to short emoji id"""
    m = re.search(":[A-Za-z0-9]*:", raw_emoji_id)
    return m.group(0)


def save_emoji_config(raw_emoji_ids):
    """Save the emoji mana config"""
    try:
        with open(EMOJI_CONFIG_PATH, "r") as file:
            emoji_config = json.load(file)
    except FileNotFoundError:
        # if no mana config file is found initialize a new one
        emoji_config = create_config_json()

    for raw_emoji_id in raw_emoji_ids:

        short_emoji_id = parse_raw_emoji_id(raw_emoji_id)

        if short_emoji_id in MANA_ID_DICT:
            emoji_config[short_emoji_id] = {
                    "web_id": MANA_ID_DICT[short_emoji_id],
                    "discord_raw_id": raw_emoji_id
                }
        else:
            raise KeyError("Short Discord emoji id is unknown: "
                           "{}".format(short_emoji_id))

    with open(EMOJI_CONFIG_PATH, "w") as file:
        json.dump(emoji_config, file, indent=4)

    # update MANA_DICT global
    global MANA_DICT
    MANA_DICT = load_mana_dict()
