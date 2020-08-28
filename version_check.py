import requests


VERSION = '1.0.0'


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
            print('You are using xc %s. The latest version is %s. Please consider update. ' % (current.version, latest.version))


def run():
    version_check()


if __name__ == '__main__':
    run()
