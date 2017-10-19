#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  $ERROR "ERROR: This setup command must be sourced!"
  exit
fi

# Setup environment variables
export ANALYSIS_BASE=$(dirname $DIR)
export PATH=$DIR:$PATH
export PATH=$DIR/syncfiles/pyfiles:$PATH
export PATH=$DIR/syncfiles/miscfiles:$PATH
export PYTHONPATH=$ANALYSIS_BASE:$PYTHONPATH
export PYTHONPATH=$DIR:$PYTHONPATH
export ROOT_INCLUDE_PATH=$ANALYSIS_BASE:$ROOT_INCLUDE_PATH

pushd $DIR > /dev/null
source ./root.sh
if [ -d $ANALYSIS_BASE/ProjectMetis/ ]; then
    cd $ANALYSIS_BASE/ProjectMetis/
    source ./setup.sh
else
    echo "NOTE: ProjectMetis was not found. You may want to set this up yourself."
fi
popd > /dev/null
