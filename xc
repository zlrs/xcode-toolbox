#!/usr/bin/python3
import sys
import os


def help_message():
    return """Xcode Opener
    A CLI tool that opens XCode project from Terminal. 
    Auto detect `.xcodeproj` file or `.xcworkspace` file. 
    For example, use it to quickly open a workspace after `pod install`. 

Usage:
    xc [<XCode_project_directory>]

Options:
    -h, --help                  Show this help"""


def getXCodeProjectOrWorkspaceFilePath(dirPath):
    workspace_ext = '.xcworkspace'
    proj_ext = '.xcodeproj'
    workspaceFile = ''
    projectFile = ''
    for entry in os.listdir(dirPath):
        if(entry.endswith(workspace_ext)):
            workspaceFile = os.path.join(dirPath, entry)
        elif entry.endswith(proj_ext):
            projectFile = os.path.join(dirPath, entry)

    if workspaceFile:
        return workspaceFile
    elif projectFile:
        return projectFile
    else:
        return ''


def openInXcode(dirPath):
    file_path = getXCodeProjectOrWorkspaceFilePath(dirPath)
    if file_path:
        cmd = 'open %s' % file_path
        print(cmd)
        os.system(cmd)
    else:
        print('No .xcodeproj / .xcworkspace file is found. ')


def main():
    if(len(sys.argv) <= 1 or sys.argv[1] == '.'):
        cwd = os.getcwd()
    elif(sys.argv[1] in ['-h', '--help']):
        print(help_message())
        return
    else:
        cwd = sys.argv[1]
    abs_cwd = os.path.abspath(cwd)
    openInXcode(abs_cwd)


if(__name__ == '__main__'):
    main()
