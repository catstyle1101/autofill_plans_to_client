import argparse


def parse_argv():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-l', '--list',
        help='client codes separated with comma: 1234,12345,1235123', type=str)
    args = arg_parser.parse_args()
    argv = None
    if args.list:
        argv = {item.strip() for item in args.list.split(',')}
    return argv
