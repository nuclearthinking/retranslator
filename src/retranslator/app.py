import logging

import click
import telegram

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def start():
    logger.info("Starting app")
    telegram.start_bot()


if __name__ == "__main__":
    cli()
