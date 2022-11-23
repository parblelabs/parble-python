from json import dump
from pathlib import Path
from typing import Optional

import click

from ._version import __version__
from .sdk import ParbleSDK
from .utils import Spinner


def _output(data, path: Optional[Path]):
    if not path:
        click.echo(data)
        return

    with open(path, "w") as f:
        dump(data, f)
        click.echo(f"Result saved in {path}")


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(version=__version__, prog_name="parble")
def parble():
    """
    Parble CLI tool main entrypoint
    """
    pass


@parble.group()
def file():
    """
    Group all file-related operations
    """
    pass


@file.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output path for the processing result",
)
def upload(file: Path, output: Path):
    """
    Upload and process FILE.

    This command upload the file FILE and waits for its processing to complete then returns it attributes.

    If waiting for the processing timed-out on the server side (300s) it will return a redirection to the file
    and the command will return the (incomplete) attributes of the file.

    """
    sdk = ParbleSDK()
    with Spinner():
        res = sdk.upload_path(file)
    data = res.json()
    _output(data, output)


@file.command()
@click.argument("file-id", type=str)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Save the json to this file",
)
def get(file_id, output):
    """
    Get the processing result of the given FILE_ID
    """
    sdk = ParbleSDK()
    res = sdk.get_file(file_id)
    data = res.json()
    _output(data, output)
