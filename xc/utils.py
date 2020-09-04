import sys


def isRunInPycharm():
    return sys.gettrace() is None
