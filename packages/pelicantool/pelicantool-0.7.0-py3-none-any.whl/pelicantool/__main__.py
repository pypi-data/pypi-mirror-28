from .parser import ParserFactory
from .exceptions import ActionNotFound
import sys

def main():
    parser = ParserFactory.factory(sys.argv[1:])
    action = parser.instance()

    if action:
        action.run()
    else:
        raise ActionNotFound
