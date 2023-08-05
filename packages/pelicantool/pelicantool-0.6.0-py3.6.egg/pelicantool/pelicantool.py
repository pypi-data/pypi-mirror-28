from . import ParserFactory
from .exceptions import ActionNotFound
import sys

def main():
    print("Hello")
    # parser = ParserFactory.factory(sys.argv[1:])
    # action = parser.instance()
    #
    # if action:
    #     action.run()
    # else:
    #     raise ActionNotFound()


# if __name__ == '__main__':
#     main()
