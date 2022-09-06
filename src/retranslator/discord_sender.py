import io

import aiohttp
from discord import File, Webhook
from settings import settings


async def send_photo(
    photo: io.BytesIO,
    file_name: str,
    message: str,
):
    async with aiohttp.ClientSession() as session:
        hook = Webhook.from_url(
            url=settings.DISCORD_WEBHOOK,
            bot_token=settings.DISCORD_TOKEN,
            session=session,
        )
        img = File(fp=photo, filename=file_name)
        await hook.send(
            file=img,
            content=message,
            wait=True,
            suppress_embeds=True,
        )


async def send_text(text: str):
    async with aiohttp.ClientSession() as session:
        hook = Webhook.from_url(
            url=settings.DISCORD_WEBHOOK,
            bot_token=settings.DISCORD_TOKEN,
            session=session,
        )
        await hook.send(
            content=text,
            wait=True,
            suppress_embeds=True,
        )


async def send_announce(message: str, photo: io.BytesIO = None) -> None:
    async with aiohttp.ClientSession() as session:
        img = File(fp=photo, filename="img.jpg") if photo else None
        hook = Webhook.from_url(
            url=settings.DISCORD_WEBHOOK,
            bot_token=settings.DISCORD_TOKEN,
            session=session,
        )

        await hook.send(file=img, content=message, wait=True, suppress_embeds=True)
