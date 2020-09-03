import requests
import os
import json
from xc.logger import printInfo, printExecute
from . import __version__

VERSION_CHECK_TIMES = 7

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
PURPLE = '\033[0;35m'
NC = '\033[0m'  # No Color

Error = f"{RED}[Error] "
Info = f"{GREEN}[Info] "
Execute = f"{PURPLE}[Execute] "


class YQVersion:
    def __init__(self, version: str):
        version.strip()
        version.strip("vV")
        self.version = version
        self.semantic_versions = version.split('.')
        self.digitVersions = []
        for semantic_ver in self.semantic_versions:
            self.digitVersions.append(int(semantic_ver))
    
    def __eq__(self, other):
        return tuple(self.digitVersions) == tuple(other.digitVersions)
    
    def __lt__(self, other):
        return tuple(self.digitVersions) < tuple(other.digitVersions)


def getLatestVersion():
    releases_API_URL = 'https://api.github.com/repos/zlrs/xcode-opener/releases?accept=application/vnd.github.v3+json'
    res = requests.get(releases_API_URL)
    if not res.ok:
        return '', f"error: status {res.status_code}"  # May be 403: exceeded API rate limit for current IP.
    
    try:
        obj = res.json()
        latest_version = obj[0]["tag_name"]
        return latest_version, None
    except:
        return '', "error"


def checkVersion():
    latest_version_str, err = getLatestVersion()
    if not err:
        current = YQVersion(__version__)
        latest = YQVersion(latest_version_str)
        if latest > current:
            printInfo('You are using xc %s. The latest version is %s. ' % (current.version, latest.version))
            res = input(Info + 'Would you like to upgrade now? [y/N]' + NC)
            if res == 'y':
                install_script = os.path.join(os.path.dirname(__file__), '../install.sh')
                install_script = os.path.expanduser(install_script)
                printExecute(install_script)
                os.execv(install_script, (install_script,))


def shouldCheckVersion():
    """
    Check version every several times(VERSION_CHECK_TIMES) the program is called.
    :return:Boolean value, whether should program check version.
    """
    def initVersionCheck(file_path):
        init_data = {
            "version_check_count": 1
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(init_data, f)

    folder = os.path.expanduser('~/.xc')
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    file_path = os.path.join(folder, 'version_check.json')
    if not os.path.exists(file_path):
        initVersionCheck(file_path)
    else:
        try:
            with open(file_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data["version_check_count"] += 1
                f.seek(0)
                json.dump(data, f)
        except:
            initVersionCheck(file_path)
    
    if data["version_check_count"] % VERSION_CHECK_TIMES == 0:
        return True
    return False


def run():
    if shouldCheckVersion():
        checkVersion()


if __name__ == '__main__':
    run()
