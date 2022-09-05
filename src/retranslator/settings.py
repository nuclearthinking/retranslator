from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    DISCORD_WEBHOOK: str
    DISCORD_WEBHOOK_ANNOUNCE: str
    DISCORD_TOKEN: str
    CHANNEL_URl: str = "https://t.me/shenty_live"


settings = Settings()
