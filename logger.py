# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
PURPLE = '\033[0;35m'
NC = '\033[0m'  # No Color

Error = f"{RED}[Error] "
Info = f"{GREEN}[Info] "
Execute = f"{PURPLE}[Execute] "


def printInfo(content):
    print(Info + content + NC)


def printError(content):
    print(Error + content + NC)


def printExecute(content):
    print(Execute + content + NC)

