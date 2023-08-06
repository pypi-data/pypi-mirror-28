"""Main script entry point for the card-py-bot"""
import argparse
import sys

import logging
import logging.handlers

from card_py_bot.bot import BOT
import card_py_bot.config


def main():
    """Startup script for the card-py-bot"""
    parser = argparse.ArgumentParser(description="card-py-bot: a Discord bot "
                                                 "that web scrapes Magic card "
                                                 "links and embeds the "
                                                 "card's details into a "
                                                 "Discord message")

    parser.add_argument("-c", "--emoji-config-path", type=str,
                        default=card_py_bot.config.EMOJI_CONFIG_PATH,
                        dest="emoji_config_path",
                        help="Path to the card-py-bot emoji_config.json to be "
                             "loaded/generated from (default: %(default)s)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--token", type=str,
                       help="String of the Discord token for the bot")
    group.add_argument("-tf", "--token-file", type=str, dest="token_file",
                       help="Path to file containing the Discord token for "
                            "the bot")

    group = parser.add_argument_group(title="Logging config")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")
    group.add_argument("-f", "--log-dir", dest="logdir",
                       help="Enable time rotating file logging at "
                            "the path specified")
    group.add_argument("-d", "--debug", action="store_true",
                       help="Enable DEBUG logging level")

    args = parser.parse_args()

    # initialize logging
    handlers = list()
    if args.logdir is not None:
        handlers.append(
            logging.handlers.TimedRotatingFileHandler(
                args.logdir,
                when="D",
                interval=1,
                backupCount=45
            )
        )

    if args.verbose:
        handlers.append(logging.StreamHandler())
    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

    # set the emoji config path
    card_py_bot.config.EMOJI_CONFIG_PATH = args.emoji_config_path

    # read the token file and extract the token
    if args.token_file is not None:
        token_file = open(args.token_file, "r")
        token = str(token_file.read()).strip()
        token_file.close()
    elif args.token is not None:
        token = args.token

    # run the bot
    BOT.run(token)

    return 0


if __name__ == "__main__":
    sys.exit(main())
