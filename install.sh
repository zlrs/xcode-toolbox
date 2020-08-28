#!/bin/zsh

repo_folder="/usr/local/xc"
command_path="/usr/local/bin/xc"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

Error="${RED}[Error] "
Info="${GREEN}[Info] "
Execute="${PURPLE}[Execute] "


if [ ! -d "/usr/local/xc" ]  # 不存在xc文件夹
then
    # clone repo
    echo "${Execute}git clone https://github.com/zlrs/xcode-opener.git $repo_folder ${NC}"
    git clone https://github.com/zlrs/xcode-opener.git $repo_folder
    
    # gen symbol link
    echo "${Info}Installing xc command to $command_path ${NC}"
    # 如果路径上已有文件，则删掉
    if [ -f $command_path ] 
    then
        echo "${Execute}rm $command_path ${NC}"
        rm $command_path
    fi
    echo "${Execute}ln -s /usr/local/xc/xc $command_path ${NC}"
    ln -s /usr/local/xc/xc $command_path
    
    echo "${Info}Installation has been completed. ${NC}"
else  # 存在 xc 文件夹
    if [ -d "/usr/local/xc/.git" ]  # 且 xc 文件夹是个git repo
    then
        echo "${Info}Already installed xc. Updating... ${NC}"
        
        echo "${Execute}cd /usr/local/xc${NC}"
        cd /usr/local/xc
        
        echo "${Execute}git pull${NC}"
        git pull
        
        if [ -f $command_path ] 
        then
            echo "${Execute}rm $command_path ${NC}"
            rm $command_path
        fi
        
        echo "${Execute}ln -s /usr/local/xc/xc $command_path ${NC}"
        ln -s /usr/local/xc/xc $command_path
    else
        echo "${Error}/usr/local/xc/ exists and is not a git repository. ${NC}"
        echo "${Error}No operation is performed. ${NC}"
        echo "${Error}Maybe you can consider remove the folder and install again?${NC}"
        exit 1
    fi
fi

# if ([ -f "$command_path" ] && [ `md5sum ./xc | cut -c 1-32` == `md5sum $command_path | cut -c 1-32` ]) then
#     echo "Installation has been completed. "
# else
#     echo "Installation failed. "
# fi
