#!/bin/bash
install_to_path="/usr/local/bin/xc"

echo "Installing xc command to $install_to_path"
cp ./xc $install_to_path

if ([ -f "$install_to_path" ] && [ `md5sum ./xc | cut -c 1-32` == `md5sum $install_to_path | cut -c 1-32` ]) then
    echo "Installation has been completed. "
else
    echo "Installation failed. "
fi
