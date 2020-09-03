#!/bin/zsh

repo_folder="/usr/local/xc"  # git clone 到这个文件夹
xc_command_script_path="$repo_folder/xc/xc"  # xc 脚本的路径
install_command_path="/usr/local/bin/xc"  # xc 脚本的安装路径

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

Error="${RED}[Error] "
Info="${GREEN}[Info] "
Execute="${PURPLE}[Execute] "


if [ ! -d "$repo_folder" ]  # 不存在xc文件夹
then
    # clone repo
    echo "${Execute}git clone https://github.com/zlrs/xcode-opener.git $repo_folder ${NC}"
    sudo -S git clone https://github.com/zlrs/xcode-opener.git $repo_folder

    # gen symbol link
    echo "${Info}Installing xc command to $install_command_path ${NC}"
    # 如果路径上已有文件，则删掉
    if [ -f $install_command_path ]
    then
        echo "${Execute}rm $install_command_path ${NC}"
        sudo -S rm $install_command_path
    fi
    echo "${Execute}ln -s $xc_command_script_path $install_command_path ${NC}"
    sudo -S ln -s $xc_command_script_path $install_command_path

    echo "${Info}Installation has been completed. ${NC}"
else  # 存在 xc 文件夹
    if [ -d "$repo_folder/.git" ]  # 且 xc 文件夹是个git repo
    then
        echo "${Info}Already installed xc. Updating... ${NC}"

        echo "${Execute}cd $repo_folder${NC}"
        cd $repo_folder || exit 2

        echo "${Execute}git pull${NC}"
        sudo -S git pull

        if [ -f $install_command_path ]
        then
            echo "${Execute}rm $install_command_path ${NC}"
            sudo -S rm $install_command_path
        fi

        echo "${Execute}ln -s $xc_command_script_path $install_command_path ${NC}"
        sudo -S ln -s $xc_command_script_path $install_command_path
    else
        echo "${Error}$repo_folder exists and is not a git repository. ${NC}"
        echo "${Error}No operation is performed. ${NC}"
        echo "${Error}Maybe you can consider remove the folder and install again?${NC}"
        exit 1
    fi
fi

# if ([ -f "$install_command_path" ] && [ `md5sum ./xc | cut -c 1-32` == `md5sum $install_command_path | cut -c 1-32` ]) then
#     echo "Installation has been completed. "
# else
#     echo "Installation failed. "
# fi
