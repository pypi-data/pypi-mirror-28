import sys
from pylogconf.core import setup


def main(
) -> None:
    """
        print all command line arguments in an explicit way.
        This can be used for testing command line programs.

        This utility doesn't use click on purpose
        :return:
    """
    setup()
    print("number of command line arguments is {}".format(len(sys.argv)))
    for i, s in enumerate(sys.argv):
        print("{}: {}".format(i, s))


if __name__ == '__main__':
    main()
