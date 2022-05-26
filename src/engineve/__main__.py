from .main import main

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('processes', nargs="?", type=str, default=None)
args = parser.parse_args(sys.argv[1:])
processes = args.processes if args.processes is not None else ["game", "graphics"]
main()