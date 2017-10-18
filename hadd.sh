#!/bin/bash

# Original Author: Samuel May
# Adopted by: P. Chang

#  .
# ..: P. Chang, philip@physics.ucsd.edu


### Function to add large numbers (>100) of histograms using hadd               ###
### hadd seems to have a limit on the number of histograms you can give it,     ###
### this adds histos in groups of 100 so you can sleep easy knowing that hadd   ###
### hasn't skipped over any of your well-deserved histograms                    ###
### Arg1: name of output histogram (e.g. "histosMaster")                        ###
### Arg2: name of input histogram (e.g. "histosToAdd_4.root" would be input     ###
###       as "histosToAdd"                                                      ###
### Arg3: number of input histograms of the above form                          ###
### Arg4: (OPTIONAL) number of cores to run on (default 1)                      ###

usage()
{
    echo "Usage:"
    echo ""
    echo "  $(basename $0) HADD_OUTPUT_NAME INPUTFILES_PREFIX NINPUTS [NCORE]"
    echo ""
    echo ""
    echo "Arg1: name of output histogram (e.g. \"histosMaster\")                                   "
    echo "Arg2: name of input histogram (e.g. \"histosToAdd_4.root\" would be input \"histosToAdd\""
    echo "Arg3: number of input histograms of the above form                                       "
    echo "Arg4: (OPTIONAL) number of cores to run on (default 1)                                   "
    exit
}

if [ -z $1 ]; then usage; fi
if [ -z $2 ]; then usage; fi
if [ -z $3 ]; then usage; fi

if (( $# < 4 ))
then
  nPar=1
else
  nPar=$4
fi

histosToAdd=""
bigHistos=""
idx1=1
idx2=1
while (($idx1 < $3))
do
  for ((i=1; i<=100; i++))
  do
    if (($idx1 <= $3))
    then
      histosToAdd=$histosToAdd" "$2"_"$idx1".root"
      let "idx1++"
    fi
  done
  hadd -f -k $1"_"$idx2".root" $histosToAdd &
  if (($idx2 % $nPar == 0))
  then
    wait
  fi
  bigHistos=$bigHistos" "$1"_"$idx2".root"
  histosToAdd=""
  let "idx2++"
done
wait
hadd -f -k $1".root" $bigHistos
