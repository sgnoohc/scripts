#!/bin/env python

import sys

filename = sys.argv[1]
instance = sys.argv[2]

f = open(filename)

funcs = []
for line in f.readlines():
    if line.strip()[:2] == "//":
        continue
    if line.find("{}.".format(instance)) != -1:
        for item in line.split("{}.".format(instance))[1:]:
            funcs.append(item.split("(")[0].strip())
funcs = list(set(funcs))

funcs.sort()
for item in funcs:
    print item
