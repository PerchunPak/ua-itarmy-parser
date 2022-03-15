"""File for ``client`` variable and method ``main``."""
from telethon import TelegramClient

from ua_itarmy_parser.config import config
from ua_itarmy_parser.listener import new_message_listener
from ua_itarmy_parser.logging import log

# noinspection PyTypeChecker
client = TelegramClient("anon", int(config["app"]["id"]), config["app"]["hash"]).start(phone=config["app"]["phone"])
log.debug("client variable initialised.")


async def main() -> None:
    client.add_event_handler(new_message_listener)
    log.warning("Going to idle, use CTRL C to stop.")
    await client.run_until_disconnected()
