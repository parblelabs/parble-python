from pathlib import Path
from typing import Optional

import click

from ._version import __version__
from .models import File
from .sdk import ParbleSDK
from .utils import Spinner


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
        file = sdk.upload_path(file)

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
    file = sdk.get_file(file_id)

    _output(file, output_format, output)
