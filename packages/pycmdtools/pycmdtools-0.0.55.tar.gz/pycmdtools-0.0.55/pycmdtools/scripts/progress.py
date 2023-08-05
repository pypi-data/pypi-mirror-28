import click
from pylogconf.core import setup

"""
enable to show progress by pointing to a FILE and not a PROCESS NAME or PID.
If you point to a file then something like fuser(1) should be called
on the file, and if there is just one process holding the file open
then show the progress on that file.

References:
- https://unix.stackexchange.com/questions/66795/how-to-check-progress-of-running-cp
- https://github.com/Xfennec/progress
- https://gist.github.com/azat/2830255
- https://stackoverflow.com/questions/10980689/how-to-follow-the-progress-of-a-linux-command
"""


@click.command()
def main(
) -> None:
    """
    follow the progress of another process
    :return:
    """
    setup()


if __name__ == '__main__':
    main()

