#!/usr/bin/env python
import argparse
from ethminer_supervisor.util import check, configure_logging, restart


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--restart', '-R', action='store_true')
parser.add_argument('--delta', '-D', type=int, default=3*60)
parser.add_argument('--log_path', '-L')


def main():
    """ CLI entry point where args are passed via `ethminer_supervisor`"""
    args = parser.parse_args()
    kwargs = {}
    if args.log_path:
        kwargs['path'] = args.log_path
    configure_logging(**kwargs)

    has_recent = check(args.delta)
    if args.restart and not has_recent:
        restart()


if __name__ == "__main__":
    main()
