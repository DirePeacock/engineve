from .main import main

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', default=False)
parser.add_argument('--demo', action='store_true', default=False)
args = parser.parse_args(sys.argv[1:])

if not args.demo:
    main(debug=args.debug)
else:
    from .rich_demo_ge import rich_main
    rich_main(debug=args.debug)