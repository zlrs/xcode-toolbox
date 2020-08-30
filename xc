#!/usr/bin/python3
import sys
import os
import shutil
import click
import version_check


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
            print('Invalid Argument: please enter a valid index. ')
            print(e)
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
        print(cmd)
        os.system(cmd)
    else:
        print('No .xcodeproj / .xcworkspace file is found. ')


def removeProjectDerivedData(inputPath, rmAll=False, rmBuild=False, rmIndex=False):
    """Remove directories from the project's derived data.
    Specifically the `Index` directory, `Build` directory, or all directories.
    """
    def removeDirIfExist(rmDirPath, ignore_errors=False):
        if os.path.exists(rmDirPath) and os.path.isdir(rmDirPath):
            print('Removing directory: ' + rmDirPath)
            shutil.rmtree(rmDirPath, ignore_errors=ignore_errors)
            return rmDirPath
        return None

    def handleRemoveSingleProject(singleProjPath, rmAll=False, rmBuild=False, rmIndex=False):
        proj_index_dir = os.path.join(singleProjPath, 'Index')
        proj_build_dir = os.path.join(singleProjPath, 'Build')
        if rmAll:
            removeDirIfExist(singleProjPath)
        else:
            if rmIndex:
                removeDirIfExist(proj_index_dir)
            if rmBuild:
                removeDirIfExist(proj_build_dir)

    def chooseFromPrompt(candidates: list) -> list:
        index_offset = 1
        lines = ['Choose the project to operate on:']
        for i, candidate in enumerate(candidates, start=index_offset):
            _line = f'{i}. {candidate}'
            lines.append(_line)
        lines.append('ALL: all above.\n')

        prompt = '\n'.join(lines)
        cmd = input(prompt)
        if cmd.isnumeric():
            idx = int(cmd) - index_offset
            if 0 <= idx < len(candidates):
                return [candidates[idx]]
        elif cmd == 'ALL':
            return candidates
        return []

    derived_data_path = os.path.expanduser('~/Library/Developer/Xcode/DerivedData/')

    proj_file_path = getXCodeProjectOrWorkspaceFilePath(inputPath)
    proj_name = os.path.splitext(os.path.basename(proj_file_path))[0]
    if proj_name is None or len(proj_name) < 1:
        return 1

    # Scan XCode derivedData folder to find out the candidate project(s) that we may need to
    # do remove operation on.
    candidates = []
    for proj_dir in os.listdir(derived_data_path):
        if proj_dir.startswith(proj_name):
            candidates.append(os.path.join(derived_data_path, proj_dir))

    # Decide the part of project(s) in `candidates` to we really to do remove operation
    chosen_ones = []
    if len(candidates) == 1:
        chosen_ones = list(candidates[0])
    elif len(candidates) > 1:
        chosen_ones = chooseFromPrompt(candidates)

    # Handle the removing all chosen projects
    for chosen_candidate in chosen_ones:
        handleRemoveSingleProject(chosen_candidate, rmAll=rmAll, rmBuild=rmBuild, rmIndex=rmIndex)

    return 0


# developer note: click option name must be lower case
@click.command()
@click.argument('path', default='.')
@click.option('--rmall', is_flag=True)
@click.option('--rmbuild', is_flag=True)
@click.option('--rmindex', is_flag=True)
def xc(path, rmall, rmbuild, rmindex):
    """A CLI tool that opens XCode project from Terminal. 
    Auto detect `.xcodeproj` file or `.xcworkspace` file. 
    For example, use it to quickly open a workspace after `pod install`. 
    """
    abs_path = os.path.expanduser(path)
    
    exit_val = 0
    if os.path.exists(abs_path):
        if rmall or rmbuild or rmindex:
            removeProjectDerivedData(abs_path, rmAll=rmall, rmBuild=rmbuild, rmIndex=rmindex)
        else:
            openInXcode(abs_path)
    else:
        click.echo('input path not exist.')
        exit_val = 1
    
    version_check.run()
    exit(exit_val)


if __name__ == '__main__':
    xc()
