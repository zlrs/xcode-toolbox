#!/usr/bin/python3
import sys
import os
import click


def getXCodeProjectOrWorkspaceFilePath(dirPath) -> str:
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
        prompt += 'please choose a file to open: '
        try:
            index = int(input(prompt))
            return files[index - 1]
        except (ValueError, IndexError) as e:
            print('Invalid Argument: please enter a valid index. ')
            exit(1)
        return ''

    workspace_ext = '.xcworkspace'
    proj_ext = '.xcodeproj'
    workspaceFile = []
    projectFile = []
    for entry in os.listdir(dirPath):
        if(entry.endswith(workspace_ext)):
            _aWorkspaceFile = os.path.join(dirPath, entry)
            workspaceFile.append(_aWorkspaceFile)
        elif entry.endswith(proj_ext):
            _aProjectFile = os.path.join(dirPath, entry)
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


def openInXcode(dirPath):
    file_path = getXCodeProjectOrWorkspaceFilePath(dirPath)
    if file_path:
        cmd = 'open "%s"' % file_path
        print(cmd)
        os.system(cmd)
    else:
        print('No .xcodeproj / .xcworkspace file is found. ')


@click.command()
@click.argument('path', default='.')
def xc(path=''):
    """A CLI tool that opens XCode project from Terminal. 
    Auto detect `.xcodeproj` file or `.xcworkspace` file. 
    For example, use it to quickly open a workspace after `pod install`. 
    """
    if path == '':
        path = os.getcwd()
    
    abs_path = os.path.abspath(path)
    
    if os.path.exists(abs_path):
        openInXcode(abs_path)
    else:
        click.echo('path not exist.')
        exit(1)


if __name__ == '__main__':
    xc()
