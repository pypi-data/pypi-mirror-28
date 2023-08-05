#!/usr/bin/env python
import argparse

from ethminer_supervisor.util import check, restart


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--restart', '-R', action='store_true')
parser.add_argument('--mock', '-M', action='store_true')


def main():
    """ CLI entry point where args are passed via `ethminer_supervisor`"""
    args = parser.parse_args()
    has_recent = check()
    if args.restart and not has_recent:
        if args.mock:
            print('Mocking restart service')
        else:
            restart()
