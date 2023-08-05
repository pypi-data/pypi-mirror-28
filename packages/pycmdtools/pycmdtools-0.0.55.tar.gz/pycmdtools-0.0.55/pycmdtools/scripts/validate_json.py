import json
from typing import List

import click
from pylogconf.core import setup


@click.command()
@click.argument(
    'args',
    required=True,
    nargs=-1,
)
def main(
        args: List[str],
) -> None:
    """
    Validate json files
    :param args: files to validate
    :return: nothing
    """
    setup()
    for filename in args:
        with open(filename, "rt") as input_handle:
            json.load(input_handle)


if __name__ == '__main__':
    main()

