#!/bin/env python

import os
import sys
import ROOT as r

def printsf(funcname, xthreshs, ythreshs, sfs, errs, filename="", xvar="eta", yvar="pt", xvarabs=False, yvarabs=False):
    """
    Function to print scale factors (or fake rate) from arrays of numbers
    """
    # parse some options and process some stuff
    yvarabsstr = ""
    xvarabsstr = ""
    if yvarabs: yvarabsstr = "fabs"
    if xvarabs: xvarabsstr = "fabs"

    # Form the function sring
    funcstr = ""
    funcstr += "float {}(float {}, float {}, int isyst=0)\n".format(funcname, yvar, xvar)
    funcstr += "{\n"
    funcstr += "    if (isyst != 1 && isyst != -1 && isyst != 0)"
    funcstr += "        printf(Form(\"WARNING - in function=%s, isyst=%d is not recommended!\n\", __FUNCTION__, isyst));"
    for i, xthresh in enumerate(xthreshs):
        for j, ythresh in enumerate(ythreshs):
            sf = sfs[i][j]
            err = errs[i][j]
            funcstr += "    if ({}({}) < {} && {}({}) < {}) return {} + isyst * {};\n".format(yvarabsstr, yvar, ythresh, xvarabsstr, xvar, xthresh, sf, err)
    funcstr += "    return 1;\n"
    funcstr += "}\n"

    # print or write to file
    if len(filename) != 0:
        f = open(filename, "w")
        f.write(funcstr)
    else:
        print funcstr

def printsf_th2(funcname, th2, filename="", xvar="eta", yvar="pt", xvarabs=False, yvarabs=False):
    """
    Function to print scale factors (or fake rate) from TH2
    """
    sfs = []
    errs = []
    xthreshs = []
    ythreshs = []
    for i in xrange(1, th2.GetNbinsX() + 1): xthreshs.append(th2.GetXaxis().GetBinUpEdge(i))
    for i in xrange(1, th2.GetNbinsY() + 1): ythreshs.append(th2.GetYaxis().GetBinUpEdge(i))
    for i in xrange(1, th2.GetNbinsX() + 1):
        sfs.append([])
        errs.append([])
        for j in xrange(1, th2.GetNbinsY() + 1):
            sfs[i-1].append(th2.GetBinContent(i, j))
            errs[i-1].append(th2.GetBinError(i, j))

    printsf(funcname, xthreshs, ythreshs, sfs, errs, filename, xvar, yvar, xvarabs, yvarabs)
#
#    # parse some options and process some stuff
#    yvarabsstr = ""
#    xvarabsstr = ""
#    if yvarabs: yvarabsstr = "fabs"
#    if xvarabs: xvarabsstr = "fabs"
#
#    # Form the function sring
#    funcstr = ""
#    funcstr += "float {}(float {}, float {}, int isyst=0)\n".format(funcname, yvar, xvar)
#    funcstr += "{\n"
#    funcstr += "    if (isyst != 1 && isyst != -1 && isyst != 0)"
#    funcstr += "        printf(Form(\"WARNING - in function=%s, isyst=%d is not recommended!\n\", __FUNCTION__, isyst));"
#    for i in xrange(1, th2.GetNbinsX() + 1):
#        for j in xrange(1, th2.GetNbinsY() + 1):
#            sf = th2.GetBinContent(i, j)
#            err = th2.GetBinError(i, j)
#            xthresh = th2.GetXaxis().GetBinUpEdge(i)
#            ythresh = th2.GetYaxis().GetBinUpEdge(j)
#            funcstr += "    if ({}({}) < {} && {}({}) < {}) return {} + isyst * {};\n".format(yvarabsstr, yvar, ythresh, xvarabsstr, xvar, xthresh, sf, err)
#    funcstr += "    return 1;\n"
#    funcstr += "}\n"
#
#    # print or write to file
#    if len(filename) != 0:
#        f = open(filename, "w")
#        f.write(funcstr)
#    else:
#        print funcstr

#def printsf_tgraph(funcname, tgraph, filename="", 

#eof
