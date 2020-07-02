import argparse

import config
import core


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=config.DESCRIPTION)
    parser.add_argument("-p", help="path to the directory", type=str)
    parser.add_argument("-i", action="store_true", help="install parsed packages")
    parser.add_argument("-ws", action="store_true", help="without python standard libs")
    parser.add_argument("-t", help="install timeout value", type=int)
    return parser


def args_parser(args: argparse.Namespace):
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
