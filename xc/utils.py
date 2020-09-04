import sys


def isRunInPycharm():
    return sys.gettrace() is not None
