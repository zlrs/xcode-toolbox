# xcode-toolbox
A CLI tool which aims to provide a convenient operation toolbox on XCode project. It's faster and cleaner than `xed`. You can use it to:

    (1) Open XCode project or workspace. 
    (2) Remove project's derived data, or just the Build or Index folder.
    (3) [WIP] Force kill XCode process. 
    (4) [WIP] Generate Objective-C function signatures.

The argument `path` is a path to the directory containing at least 1 `.xcodeproj` or `.xcworkspace` file, default 
to the current directory. `.xcworkspace` has higher priority than `.xcodeproj`.

## Installation
```shell
pip3 install xcode-toolbox
```

## Requirements
* Python 3.6+
* requests
* click

## Usage

```
Usage: xc [OPTIONS] [PATH]

  A CLI tool which aims to provide a convenient operation toolbox on XCode
  project. It's faster and cleaner than `xed`. You can use it to: (1) open
  XCode project or workspace. (2) remove project's derived data. (3) [WIP]
  force kill XCode process. (4) [WIP] generate Objective-C function
  signatures.

  The argument `path` is a path to the directory containing at least 1
  `.xcodeproj` or `.xcworkspace` file, default to the current directory.
  `.xcworkspace` has higher priority than `.xcodeproj`.

  Contribute: https://github.com/zlrs/xcode-opener

Options:
  --rm-all    Remove the project's derived data in
              ~/Library/Developer/Xcode/DerivedData.

  --rm-build  Similar to --rm-all, but only remove the `Build` subdirectory.
  --rm-index  Similar to --rm-all, but only remove the `Index` subdirectory.
  --help      Show this message and exit.
```

## Example
1. open a XCode project or workspace
    * specify folder explicitly
    ```shell
    git clone git@github.com:SDWebImage/SDWebImage.git ~/GitHub
    xc ~/GitHub/SDWebImage/Examples
    ```
    * open project/workspace of current folder without parameters
    ```shell
    git clone git@github.com:SDWebImage/SDWebImage.git
    cd SDWebImage/Examples
    xc
    ```
2. clear project derived folder
```
# remove project's index from derived data
xc <Path> --rm-index

# remove project's build from derived data
xc <Path> --rm-build

#remove project's all derived data
xc <Path> --rm-all
```

## Todo features
- [ ] toolbox subcommands
    - [ ] `kill` subcommand. To kill all running XCode processes, equivalent to the following shell command. 
    ```shell
    kill $(ps aux | grep 'Xcode' | awk '{print $2}')
    ```
    - [ ] `find` subcommand. Find a source file/project file(s) under the given directory tree. 
    - [ ] generate Objective-C method signature.
- [x] clear XCode project index folder
- [x] clear XCode project derivedData folder

## Contribution
Comments, pull requests or other kind of contributions are welcome! 

Also if you have any requirements or you encounter any bugs, feel free to open an issue or create a pull request!

## LICENSE
MIT @ zlrs
