import logging
from pathlib import Path
from typing import Optional

import click

from ._version import __version__
from .exceptions import APICallError, ConfigurationError
from .models import File
from .sdk import ParbleSDK
from .utils import Spinner

NAME = "parble"

logger = logging.getLogger(NAME)


class ClickFormatter(logging.Formatter):
    colors = {
        "exception": dict(fg="red"),
        "critical": dict(fg="red"),
        "error": dict(fg="red"),
        "warning": dict(fg="yellow"),
        "info": dict(fg="green"),
        "debug": dict(fg="blue"),
    }

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Use click style to customize the log message
        """
        level = record.levelname.lower()
        msg = super().formatMessage(record)

        if level in self.colors:
            prefix = click.style("{}: ".format(level), **self.colors[level])
            return prefix + msg
        return msg


class ClickHandler(logging.Handler):
    def emit(self, record):
        """
        Emit records using click, so it can handle streams for us
        """
        try:
            msg = self.format(record)
            click.echo(msg, err=True)
        except Exception:
            self.handleError(record)


def _output(file: File, output_format: str, path: Optional[Path] = None):
    if output_format == "pdf":
        data = file.pdf.read()
    else:
        data = file.json().encode()

    if not path:
        click.echo(data)
        return

    with open(path, "wb") as f:
        click.echo(data, f)

    click.echo(f"Result saved in {path}")


class ParbleGroup(click.Group):
    def main(self, *args, **kwargs):
        try:
            return super().main(*args, **kwargs)
        except ConfigurationError as e:
            logger.error("Parble SDK Configuration Error!")
            logger.error(e)
            logger.debug("Exception info:", exc_info=1)
        except APICallError as e:
            logger.error("Parble API returned an error!")
            logger.error(e)
            logger.debug("Exception info:", exc_info=1)
        except Exception as e:
            logger.error("An SDK error occurred!")
            logger.error(e)
            logger.debug("Exception info:", exc_info=1)


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, cls=ParbleGroup)
@click.version_option(version=__version__, prog_name="parble")
@click.option("-v", "--verbose", count=True, help="Increase the verbosity. Can be stacked (-vvv)")
def parble(verbose):
    """
    Parble CLI tool

    \b
    The CLI relies on the following 2 environment variables:
    - PARBLE_URL: URL of the tenant to use
    - PARBLE_API_KEY: API-Key to use

    They must be exported and available in the shell where the command is invoked.
    """
    log = logging.getLogger(NAME)
    # each verbosity count increases the log level up to debug
    log.setLevel(max(logging.DEBUG, logging.ERROR - verbose * 10))
    hdl = ClickHandler()
    hdl.formatter = ClickFormatter()
    log.handlers = [hdl]
    log.propagate = False


@parble.group()
def file():
    """
    Group all file-related operations
    """
    pass


@file.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["pdf", "json"]),
    default="json",
    help="Output format",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Save the output to this file",
)
def upload(file: Path, output: Path, output_format: str):
    """
    Upload and process FILE.

    This command upload the file FILE and waits for its processing to complete then returns it attributes.

    If waiting for the processing timed-out on the server side (300s) it will return a redirection to the file
    and the command will return the (incomplete) attributes of the file.

    """
    sdk = ParbleSDK()
    with Spinner():
        file = sdk.files.post(file)

    _output(file, output_format, output)


@file.command()
@click.argument("file-id", type=str)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["pdf", "json"]),
    default="json",
    help="Output format",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Save the output to this file",
)
def get(file_id, output, output_format):
    """
    Get the processing result of the given FILE_ID
    """
    sdk = ParbleSDK()
    file = sdk.files.get(file_id)

    _output(file, output_format, output)
