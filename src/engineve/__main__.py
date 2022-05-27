from .main import main

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', default=False)
args = parser.parse_args(sys.argv[1:])

main(debug=args.debug)