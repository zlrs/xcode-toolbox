import requests
import os
import json

VERSION = '1.1.0'


class Version:
    def __init__(self, version: str):
        version.strip()
        version.strip("vV")
        self.version = version
        self.sematic_versions = version.split('.')
        self.digitVersions = []
        for sematic_ver in self.sematic_versions:
            self.digitVersions.append(int(sematic_ver))
    
    def __eq__(self, other):
        return tuple(self.digitVersions) == tuple(other.digitVersions)
    
    def __lt__(self, other):
        return tuple(self.digitVersions) < tuple(other.digitVersions)


def get_latest_version():
    URL = 'https://api.github.com/repos/zlrs/xcode-opener/releases?accept=application/vnd.github.v3+json'
    res = requests.get(URL)
    if not res.ok:
        return '', "error"
    
    try:
        obj = res.json()
        latest_version = obj[0]["tag_name"]
        return latest_version, None
    except:
        return '', "error"


def version_check():
    latestVersionStr, err = get_latest_version()
    if not err:
        current = Version(VERSION)
        latest = Version(latestVersionStr)
        if latest > current:
            print('You are using xc %s. The latest version is %s. Please consider upgrade. ' % (current.version, latest.version))
            print('https://github.com/zlrs/xcode-opener/releases')


def shouldCheckVersion():
    def initVersionCheck(file_path):
        data = {
            "version_check_count": 1
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

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
    
    if data["version_check_count"] % 10 == 0:
        return True
    return False


def run():
    if shouldCheckVersion():
        version_check()


if __name__ == '__main__':
    run()
