"""Module for parsing the WOTC website for data on magic cards"""

import re
from logging import getLogger
from urllib.request import urlopen

import lxml
import discord
from bs4 import BeautifulSoup

import card_py_bot.config
from card_py_bot import WIZARDS_BASE_URL

__log__ = getLogger(__name__)


CARD_ELEMENT_LIST = [
    "Mana Cost",
    "Types",
    "Rarity",
    "Card Text",
    "Flavor Text",
    "P/T",
    "Expansion",
    "Artist",
    "image_url"
]


def parse_cardtextbox(cardtextbox_div) -> str:
    """Parse an arbitrary text box and also extract elements like mana"""
    def extract_content(content):
        content_string_ = ""
        try:
            icon_content = content["alt"]
            icon_string = card_py_bot.config.MANA_DICT[icon_content].strip()
            return " {} ".format(icon_string)
        except (TypeError, KeyError):
            pass

        try:
            for content_prt in content.contents:
                content_string_ += extract_content(content_prt)
        except AttributeError:
            return content
        return content_string_

    content_string = extract_content(cardtextbox_div)

    # cleaning content_string for random newlines
    content_string = content_string.lstrip("\\n").strip()
    return content_string


def parse_base_value(value_div) -> str:
    """Parse out a simple element like an label value name"""
    value_string = value_div.string.strip()
    value_string = re.sub("â€”", "--- ", value_string)
    return value_string


def parse_mana(mana_div) -> str:
    """Parse the mana cost of a card"""
    mana_string = ""
    for mana_content in mana_div.children:
        try:
            mana_string += card_py_bot.config.MANA_DICT[mana_content["alt"]].strip() + " "
        except TypeError:
            pass
    return mana_string


def parse_image(image_div) -> str:
    """Parse the handler url for a card's image"""
    image_handler = image_div.img["src"].lstrip("../../")
    return image_handler


def parse_rarity(rarity_div) -> str:
    """Parse the rarity of a card"""
    rarity = rarity_div.span.string
    return rarity


def parse_artist(artist_div) -> str:
    """Parse the artist name of a card"""
    artist = artist_div.a.string
    return artist


def parse_expansion(expansion_div) -> str:
    """Parse the expansion name and set image handler"""
    second_a = expansion_div.findAll("a")[1].text
    return second_a
    # return WIZARDS_BASE_URL + expansion_div.find("img")["src"].lstrip("../../")


LABEL_DICT = {
    "Community Rating": "skip",
    "Card Name": parse_base_value,
    "Mana Cost": parse_mana,
    "Converted Mana Cost": parse_base_value,
    "Types": parse_base_value,
    "Card Text": parse_cardtextbox,
    "P/T": parse_base_value,
    "Expansion": parse_expansion,
    "Rarity": parse_rarity,
    "All Sets": "skip",
    "Card Number": parse_base_value,
    "Artist": parse_artist,
    "Flavor Text": parse_cardtextbox,
}


def scrape_card(url: str) -> dict:
    """Scrape a WOTC magic card webpage and extract the cards details for
    embedding into a Discord message"""
    __log__.debug("Scraping WOTC Magic card at: {}".format(url))

    soup = BeautifulSoup(urlopen(url), "lxml")

    card_data = dict()
    label_list = soup.find_all("div", class_="label")
    for label_div in label_list:
        for string in label_div.stripped_strings:
            label_name = string.strip(":")
            if label_name in LABEL_DICT and LABEL_DICT[label_name] != "skip":
                card_data[label_name] = \
                    LABEL_DICT[label_name](label_div.find_next_sibling("div"))

    card_image_div = soup.find("div", class_="cardImage")
    card_data["image_url"] = WIZARDS_BASE_URL + parse_image(card_image_div)
    return card_data


def create_card_embed(card_data: dict, card_url: str) -> discord.Embed:
    """Format scraped card data into a Discord embed"""
    try:
        card_name = card_data["Card Name"]
        embed_title = "**Card Name**\n[{}]({})".format(card_name, card_url)
    except Exception:
        embed_title = "Error: giving raw url: {}".format(card_url)

    em = discord.Embed(description=embed_title, colour=0xDEADBF)

    for element in CARD_ELEMENT_LIST:
        if element in card_data:
            if element == "image_url":
                em.set_image(url=card_data[element])
            elif element == "Flavor Text":
                em.add_field(
                    name=element,
                    value="*{}*".format(card_data[element])
                )
            else:
                em.add_field(
                    name=element,
                    value=card_data[element],
                    inline=False
                )
    return em


def embed_card(url: str) -> discord.Embed:
    """From a Magic card url create a Discord embed"""
    return create_card_embed(scrape_card(url), url)
