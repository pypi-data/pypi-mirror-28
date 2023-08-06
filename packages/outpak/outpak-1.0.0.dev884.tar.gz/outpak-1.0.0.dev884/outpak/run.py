"""Outpak main module."""
import os
import click
from outpak import __version__
from buzio import console
from outpak.main import Outpak

def get_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'pak.yml'
    )

@click.command()
@click.option(
    '-c',
    envvar="OUTPAK_FILE",
    help='Full path for configuration file.',
    default=get_path,
    type=click.Path(exists=True))
def install(c):
    """Run main command for cabrita.

    1. Check version
    2. Import configuration file
    3. Run dashboard.
    """
    console.box("Outpak v{}".format(__version__))
    newpak = Outpak(c)
    newpak.run()

if __name__ == "__main__":
    install()