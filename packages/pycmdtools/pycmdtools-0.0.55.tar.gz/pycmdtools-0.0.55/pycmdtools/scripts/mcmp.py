import collections
import hashlib
import functools
from typing import List

import click
from pylogconf.core import setup
from tqdm import tqdm


"""
TODO:
- make the algorithm faster by looking only at the beginning of the files.
- make the algorithm faster by looking at the length of the files.
- make the algorithm faster by having a gnu dbm ~/.mcmp which already stores
    hashes of known files.
"""


def checksum(file_name: str=None, algorithm: str=None) -> str:
    """
    calculate a checksum of a file. You dictate which algorithm.
    If you want to see all algorithms try:
    hashlib.algorithms_available
    :param file_name:
    :param algorithm:
    :return:
    """
    block_size = 65536
    with open(file_name, mode='rb') as f:
        hash_object = hashlib.new(algorithm)
        for buf in iter(functools.partial(f.read, block_size), b''):
            hash_object.update(buf)
    return hash_object.hexdigest()


@click.command()
@click.option(
    '--algorithm',
    required=False,
    default='md5',
    type=click.Choice(hashlib.algorithms_available),
    help="algorithm to use",
    show_default=True,
)
@click.option(
    '--progress',
    required=False,
    default=True,
    type=bool,
    help="show progress report",
    show_default=True,
)
@click.argument(
    'files',
    nargs=-1,
    required=True,
)
def main(
        algorithm: str,
        progress: bool,
        files: List[str],
) -> None:
    """
    compare many files and print identical ones
    :param algorithm:
    :param progress:
    :param files: 
    :return: 
    """
    setup()
    d = collections.defaultdict(set)
    if progress:
        files = tqdm(files)
    for file_name in files:
        check_sum = checksum(file_name=file_name, algorithm=algorithm)
        d[check_sum].add(file_name)
    for i, check_sum in enumerate(sorted(d.keys())):
        print("{}: {}".format(i, ", ".join(sorted(d[check_sum]))))


if __name__ == '__main__':
    main()
