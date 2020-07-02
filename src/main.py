import argparse
import sys

from src import config, core


class ArgParser(argparse.ArgumentParser):
    """
    Class for print help message when arguments doesn't given
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def init_parser() -> argparse.ArgumentParser:
    """
    Init arguments parser

    :return:
    """
    parser = ArgParser(description=config.DESCRIPTION)
    parser.add_argument("-p", help="path to the directory", type=str, required=True)
    parser.add_argument("-i", action="store_true", help="install parsed packages")
    parser.add_argument("-ws", action="store_true", help="parse without python standard libs")
    parser.add_argument("-t", help="install timeout value", type=int)
    return parser


def args_parser(args: argparse.Namespace):
    """
    Parsing given arguments

    :param args:
    :return:
    """
    if len(sys.argv) == 1:
        PARSER.print_help(sys.stderr)
    else:
        imports = None
        if args.t:
            config.INSTALL_TIMEOUT = args.t
        if args.p:
            imports = core.get_imports(args.p, args.ws)
        if args.i and imports:
            core.install_libs(imports)


if __name__ == '__main__':
    PARSER = init_parser()
    args_parser(PARSER.parse_args())
