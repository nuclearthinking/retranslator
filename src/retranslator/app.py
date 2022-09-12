import logging

import click
import sentry_sdk

import telegram
from settings import  settings
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0,
    )


@cli.command()
def start():
    logger.info("Starting app")
    telegram.start_bot()


if __name__ == "__main__":
    cli()
