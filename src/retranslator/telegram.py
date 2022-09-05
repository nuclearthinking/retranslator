import io
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ContentType

from retranslator import discord_sender
from retranslator.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s : %(levelname)s | %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

media_content = [ContentType.PHOTO]

text_content = [ContentType.TEXT]

video_content = [ContentType.VIDEO, ContentType.VIDEO_NOTE]

announce_emoji = ["🔜", "💜", "❤"]


def is_announce_message(text: str) -> bool:
    return any(emoji in text for emoji in announce_emoji)


class ChannelFilter(BoundFilter):
    key = "channel_id"

    def __init__(self, channel_id: int | list[int]) -> None:
        if isinstance(channel_id, int):
            self.channel_ids = [channel_id]
        self.channel_ids = channel_id

    async def check(self, message: types.Message) -> bool:
        logger.info(
            "Message from channel with id: %s, title: %s",
            message.sender_chat.id,
            message.sender_chat.title,
        )
        # return message.sender_chat.id in self.channel_ids
        return True


channel_white_list_filter = ChannelFilter(channel_id=[-1001775379988])


@dp.channel_post_handler(channel_white_list_filter, content_types=media_content)
async def handle_photo_message(message: types.Message):
    largest_photo = message.photo[-1]
    file_name = f"{largest_photo.file_unique_id}.jpg"
    file = io.BytesIO()
    await message.photo[-1].download(destination_file=file)
    if is_announce_message(message.caption):
        await discord_sender.send_announce(
            photo=file,
            message=f"{message.caption}\n{message.url}",
        )
        return
    await discord_sender.send_photo(
        photo=file, file_name=file_name, message=f"{message.url}"
    )


@dp.channel_post_handler(channel_white_list_filter, content_types=text_content)
async def handle_message(message: types.Message):
    if is_announce_message(message.text):
        await discord_sender.send_announce(
            message=f"{message.text}\n{message.url}",
        )
        return
    await discord_sender.send_text(text=f"{message.text}\n{message.url}")


@dp.channel_post_handler(channel_white_list_filter, content_types=video_content)
async def handle_video_message(message: types.Message):
    text = f"Новое видео в телеграм канале Shenty\n{message.url}"
    await discord_sender.send_text(text=text)


def start_bot():
    executor.start_polling(dp, skip_updates=True)
