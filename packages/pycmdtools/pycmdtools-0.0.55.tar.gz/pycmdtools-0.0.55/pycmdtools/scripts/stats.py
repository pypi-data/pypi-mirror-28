from typing import List

import click
from pylogconf.core import setup

from pycmdtools.utils import diamond_lines


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
)
def main(
        args: List[str],
) -> None:
    """
        Print statistics about a list of numbers.
        This currently only prints their average.
        :param args:
        :return:
    """
    setup()
    total_sum = 0.0
    total_sum2 = 0.0
    count = 0
    for line in diamond_lines(args):
        count += 1
        value = float(line)
        total_sum += value
        total_sum2 += value * value
    if count != 0:
        print(total_sum / count)
    else:
        print("no data given")


if __name__ == '__main__':
    main()
