#!/bin/bash

# goes through packages with 'Makefile' and compile

for ITEM in $(ls $ANALYSIS_BASE/*/Makefile); do
    echo 'Compiling ... '$(dirname $ITEM)
    cd $(dirname $ITEM)
    make -j 20
    cd - > /dev/null
done
