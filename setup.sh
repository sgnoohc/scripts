#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  $ERROR "ERROR: This setup command must be sourced!"
  exit
fi

export ANALYSIS_BASE=$DIR/../
pushd $DIR
export PATH=$DIR:$PATH
source ./root.sh
cd ../ProjectMetis/
source ./setup.sh
popd
