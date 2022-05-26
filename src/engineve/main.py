import logging
from .factory import factory


def main(debug=False):
    # if debug:
    #     logging.basicConfig(level=logging.DEBUG)
    client = factory()
    client.main()

if __name__ == "__main__":
    main()