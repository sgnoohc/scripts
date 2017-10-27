#!/bin/env python

import os
import sys
import ROOT as r

def printsf(funcname, th2, filename=""):
    f = None
    if len(filename) != 0:
        f = open(filename, "w")
    funcstr = ""
    funcstr += "float {}(float pt, float eta, int isyst=0)\n".format(funcname)
    funcstr += "{\n"
    funcstr += "    if (isyst != 1 && isyst != -1 && isyst != 0)"
    funcstr += "        printf(Form(\"WARNING - in function=%s, isyst=%d is not recommended!\n\", __FUNCTION__, isyst));"
    for i in xrange(1, th2.GetNbinsX() + 1):
        for j in xrange(1, th2.GetNbinsY() + 1):
            sf = th2.GetBinContent(i, j)
            err = th2.GetBinError(i, j)
            etathresh = th2.GetXaxis().GetBinUpEdge(i)
            ptthresh = th2.GetYaxis().GetBinUpEdge(j)
            funcstr += "    if (pt < {} && fabs(eta) < {}) return {} + isyst * {};\n".format(ptthresh, etathresh, sf, err)
    funcstr += "    return 1;\n"
    funcstr += "}\n"
    if f:
        f.write(funcstr)
    else:
        print funcstr

#eof
