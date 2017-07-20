#!/bin/bash

if [ -f /etc/debian_version ] ; then
    echo "Installing Debian/Ubuntu packages ..."
    # drmaa with slurm extension
    sudo apt-get install -y build-essential slurm-drmaa1 slurm-drmaa-dev slurm-llnl
elif [ -f /etc/redhat-release ] ; then
    echo "Installing RedHat/CentOS packages ..."
    #sudo yum -y install wget
elif [ `uname -s` = "Darwin" ] ; then
    echo "Installing MacOSX/Homebrew packages ..."
    #brew install wget
fi
