import os
import click
from xc import version_check
from xc.logger import printInfo, printExecute, printError
from xc.derived_data_clearner import removeProjectDerivedData
from xc.utils import isRunInPycharm
from . import __version__


def getXCodeProjectOrWorkspaceFilePath(inputPath) -> str:
    def hasSameFileName(file1: str, file2: str) -> bool:
        basename1 = os.path.basename(file1)
        basename2 = os.path.basename(file2)
        return os.path.splitext(basename1)[0] == os.path.splitext(basename2)[0]

    def chooseFromPrompt(workspaceFile: [str], projectFile: [str]) -> str:
        files = workspaceFile + projectFile
        prompt = ''
        cnt = 1
        for file in files:
            line = '%d. %s\n' % (cnt, os.path.basename(file))
            prompt += line
            cnt += 1
        prompt += 'please choose the file to operate: '
        try:
            index = int(input(prompt))
            return files[index - 1]
        except (ValueError, IndexError) as e:
            printError('Invalid Argument: please enter a valid index. ')
            printError(e)
            exit(1)
        return ''

    workspace_ext = '.xcworkspace'
    proj_ext = '.xcodeproj'
    workspaceFile = []
    projectFile = []
    for entry in os.listdir(inputPath):
        if entry.endswith(workspace_ext):
            _aWorkspaceFile = os.path.join(inputPath, entry)
            workspaceFile.append(_aWorkspaceFile)
        elif entry.endswith(proj_ext):
            _aProjectFile = os.path.join(inputPath, entry)
            projectFile.append(_aProjectFile)

    if len(workspaceFile) == 0 and len(projectFile) == 0:  # dirPath下没有XCode项目
        return ''
    elif len(workspaceFile) == 0 and len(projectFile) == 1:  # 只有1个proj文件
        return projectFile[0]
    elif len(workspaceFile) == 1 and len(projectFile) == 0:  # 只有1个workspace文件
        return workspaceFile[0]
    elif len(workspaceFile) == 1 and len(workspaceFile) == 1 and hasSameFileName(workspaceFile[0], projectFile[0]):
        return workspaceFile[0]  # 认为两文件同属一个XCode项目，忽略proj文件
    else:
        return chooseFromPrompt(workspaceFile, projectFile)  # 存在多个项目，提示用户手动选择


def openInXcode(inputPath):
    file_path = getXCodeProjectOrWorkspaceFilePath(inputPath)
    if file_path:
        cmd = 'open "%s"' % file_path
        printExecute(cmd)
        os.system(cmd)
    else:
        printInfo('No .xcodeproj / .xcworkspace file is found. ')


def removeDerivedData(inputPath, rmAll=False, rmBuild=False, rmIndex=False):
    """ Handle `--rm-` options """
    proj_file_path = getXCodeProjectOrWorkspaceFilePath(inputPath)
    if proj_file_path:
        removeProjectDerivedData(proj_file_path, rmAll=rmAll, rmBuild=rmBuild, rmIndex=rmIndex)
    else:
        printInfo('No .xcodeproj / .xcworkspace file is found. ')


# developer note: click option name must be lower case
@click.command()
@click.argument('path', default='.')
@click.option('--rm-all', is_flag=True,
              help="Remove the project's derived data in ~/Library/Developer/Xcode/DerivedData.")
@click.option('--rm-build', is_flag=True,
              help='Similar to --rm-all, but only remove the `Build` subdirectory.')
@click.option('--rm-index', is_flag=True,
              help='Similar to --rm-all, but only remove the `Index` subdirectory.')
@click.option('--version', is_flag=True)
def xc(path, rm_all, rm_build, rm_index, version):
    """A CLI tool which aims to provide a convenient operation toolbox on XCode project.
    You can use it to:
    (1) open XCode project or workspace. (2) remove project's derived data.
    (3) [WIP] force kill XCode process. (4) [WIP] generate Objective-C function signatures.

    The argument `path` is a path to the directory containing at least 1 `.xcodeproj` or `.xcworkspace` file, default
    to the current directory. `.xcworkspace` has higher priority than `.xcodeproj`.

    Contribute: https://github.com/zlrs/xcode-opener
    """
    if isRunInPycharm():
        print(f"rm_all: {rm_all}, rm_build: {rm_build}, rm_index: {rm_index}, version: {version}")

    if version:
        print(__version__)
        exit(0)

    abs_input_path = os.path.expanduser(path)
    
    exit_val = 0
    if os.path.exists(abs_input_path):
        if rm_all or rm_build or rm_index:
            removeDerivedData(abs_input_path, rmAll=rm_all, rmBuild=rm_build, rmIndex=rm_index)
        else:
            openInXcode(abs_input_path)
    else:
        click.echo('input path not exist.')
        exit_val = 1
    
    version_check.run()
    exit(exit_val)


if __name__ == '__main__':
    xc()
