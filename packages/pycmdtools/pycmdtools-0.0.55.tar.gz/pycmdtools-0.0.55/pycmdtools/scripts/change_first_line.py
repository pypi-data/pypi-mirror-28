from typing import List

import click
from pylogconf.core import setup


@click.command()
@click.option(
    '--from_line',
    required=False,
    default=None,
    type=str,
    help="from what value?",
    show_default=True,
)
@click.option(
    '--to_line',
    required=True,
    default=None,
    type=str,
    help="to what value?",
    show_default=True,
)
@click.argument(
    'filenames',
    required=True,
    nargs=-1,
)
def main(
        from_line: str,
        to_line: str,
        filenames: List[str],
) -> None:
    """
        Change the first line in files.
        :param from_line: what text to change
        :param to_line: what to change it to
        :param filenames: filenames to change the first line of
        :return: nothing
    """
    setup()
    changed = 0
    actually_changed = 0
    print("from_line is [{}]".format(from_line))
    print("to_line is [{}]".format(to_line))
    for filename in filenames:
        print("considering [{}]...".format(filename))
        with open(filename, "rt") as input_handle:
            data = input_handle.readlines()
        if len(data) == 0:
            continue
        # change the first line
        if from_line is None or data[0] == from_line+"\n":
            if data[0] != to_line+"\n":
                actually_changed += 1
            data[0] = to_line+"\n"
            changed += 1
        with open(filename, "wt") as output_handle:
            output_handle.write("".join(data))
    # print statistics
    print("changed is [{}]".format(changed))
    print("actually_changed is [{}]".format(actually_changed))


if __name__ == '__main__':
    main()

