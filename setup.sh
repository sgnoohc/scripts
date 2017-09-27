#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  $ERROR "ERROR: This setup command must be sourced!"
  exit
fi

# Setup environment variables
export ANALYSIS_BASE=$(dirname $DIR)
export PATH=$DIR:$PATH
export PYTHONPATH=$ANALYSIS_BASE:$PYTHONPATH
export PYTHONPATH=$DIR:$PYTHONPATH
export ROOT_INCLUDE_PATH=$ANALYSIS_BASE:$ROOT_INCLUDE_PATH

pushd $DIR
source ./root.sh
cd ../ProjectMetis/
source ./setup.sh
popd
