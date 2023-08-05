"""find dominated strategies"""
import argparse
import json
import sys

from gameanalysis import dominance
from gameanalysis import gamereader


def add_parser(subparsers):
    parser = subparsers.add_parser(
        'dominance', aliases=['dom'], help="""Computed dominated strategies""",
        description="""Compute dominated strategies, or subgames with only
        undominated strategies.""")
    parser.add_argument(
        '--input', '-i', metavar='<input-file>', default=sys.stdin,
        type=argparse.FileType('r'), help="""Input file for script.  (default:
        stdin)""")
    parser.add_argument(
        '--output', '-o', metavar='<output-file>', default=sys.stdout,
        type=argparse.FileType('w'), help="""Output file for script. (default:
        stdout)""")
    parser.add_argument(
        '--strategies', '-s', action='store_true', help="""Output the remaining
        strategies instead of the subgame after removing appropriate
        strategies.  (default: %(default)s)""")
    parser.add_argument(
        '--criterion', '-c', default='strictdom',
        choices=['weakdom', 'strictdom', 'neverbr'],
        help="""Dominance criterion: strictdom = strict pure-strategy
        dominance; weakdom = weak pure-strategy dominance; neverbr =
        never-best-response. (default: %(default)s)""")
    parser.add_argument(
        '--unconditional', '-u', action='store_false', help="""If specified use
        unconditional dominance, instead of conditional dominance.""")
    return parser


def main(args):
    game = gamereader.load(args.input)
    sub_mask = dominance.iterated_elimination(
        game, args.criterion, conditional=args.unconditional)
    if args.strategies:
        json.dump(game.subgame_to_json(sub_mask), args.output)
    else:
        json.dump(game.subgame(sub_mask).to_json(), args.output)

    args.output.write('\n')
