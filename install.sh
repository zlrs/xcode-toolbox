#!/bin/bash
install_to_path="/usr/local/bin/xc"
echo "Installing xc command to $install_to_path"
cp ./xc $install_to_path
if [ -f "$install_to_path" ]; then
    echo "Installation has been completed. "
else
    echo "Installation failed. "
fi

