#! /bin/bash

set -u
export SHELL_SCRIPT_MODULE_PATH="/vagrant/vagrant/modules"
source "${SHELL_SCRIPT_MODULE_PATH}/lib.sh"

runModules "base" "mysql" "python-virtualenv"