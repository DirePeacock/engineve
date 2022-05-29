import logging
import time
from .mainfactory import factory

def main(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    engine = factory(spawn=True)
    engine.main()

if __name__ == "__main__":
    main(debug=False)
    # main(debug=False)