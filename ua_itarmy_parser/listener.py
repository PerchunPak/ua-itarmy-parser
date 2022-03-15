"""Main listener file."""
from asyncio import create_task
from re import IGNORECASE, findall
from typing import List

from telethon.events import NewMessage, register

from ua_itarmy_parser.ddos import RunDDOS
from ua_itarmy_parser.logging import log


@register(NewMessage(chats="https://t.me/itarmyofukraine2022"))
async def new_message_listener(event: NewMessage.Event) -> None:
    """Listen new messages in @itarmyofukraine2022.

    Args:
        event: Required argument for Telethon event handlers.
    """
    log.info("New message received.")
    message = event.message.message

    links: List["str"] = findall(r"https?://\S*", message, IGNORECASE)
    ips: List["str"] = findall(
        r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", message
    )

    create_task(RunDDOS.init_ddos(links, ips))
