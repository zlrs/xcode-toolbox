import os
import shutil
from xc.logger import printInfo, printError
import plistlib
from typing import List, Tuple


def parsePlist(plist_file_path) -> dict:
    obj = {}
    if os.path.exists(plist_file_path):
        try:
            with open(plist_file_path, 'rb') as f:
                obj = plistlib.load(f)
        except Exception as e:
            printError(e)

    return obj


def workspacePathFromPlist(plist_file_path) -> str:
    workspacePath = ''
    try:
        obj: dict = parsePlist(plist_file_path)
        workspacePath = obj.get('WorkspacePath')
    except Exception as e:
        printError(e)

    return workspacePath


def removeProjectDerivedData(proj_file_path, rmAll=False, rmBuild=False, rmIndex=False):
    """Remove directories from the project's derived data.
    Specifically the `Index` directory, `Build` directory, or all directories.
    """
    def removeDirIfExist(rmDirPath, ignore_errors=False):
        if os.path.exists(rmDirPath) and os.path.isdir(rmDirPath):
            printInfo('Removing directory: ' + rmDirPath)
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

    def chooseFromPrompt(candidates: List[Tuple]) -> List[Tuple]:
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

    proj_name = os.path.splitext(os.path.basename(proj_file_path))[0]
    if proj_name is None or len(proj_name) < 1:
        return 1

    # Scan XCode derivedData folder to find out the candidate project(s) that we may need to
    # do remove operation on.
    candidates: List[Tuple] = []
    for proj_dir in os.listdir(derived_data_path):
        if proj_dir.startswith(proj_name):
            proj_derived_data_dir = os.path.join(derived_data_path, proj_dir)
            workspacePath = workspacePathFromPlist(os.path.join(proj_derived_data_dir, 'info.plist'))
            candidates.append((proj_derived_data_dir, workspacePath))

    # Decide the part of project(s) in `candidates` to we really to do remove operation
    # chosen_ones: List[Tuple] = []
    # if len(candidates) == 1:
    #     chosen_ones = [candidates[0]]
    # elif len(candidates) > 1:
    chosen_ones: List[Tuple] = chooseFromPrompt(candidates)

    # Handle the removing all chosen projects
    for chosen_candidate in chosen_ones:
        chosen_derived_data_path = chosen_candidate[0]
        chosen_proj_source_path = chosen_candidate[1]
        handleRemoveSingleProject(chosen_derived_data_path, rmAll=rmAll, rmBuild=rmBuild, rmIndex=rmIndex)

    return 0
