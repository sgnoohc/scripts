#!/bin/env python

#  .
# ..: P.Chang, philip@physics.ucsd.edu

# ================================================================
# Wrapper script to plottery. (https://github.com/aminnj/plottery)
# ================================================================

import ROOT as r
from plottery import plottery as p
from plottery import utils as u
import math
import sys
import uuid

########################################################################
# New TColors
########################################################################
mycolors = []
mycolors.append(r.TColor(11005 , 103 / 255. , 0   / 255. , 31  / 255.))
mycolors.append(r.TColor(11004 , 178 / 255. , 24  / 255. , 43  / 255.))
mycolors.append(r.TColor(11003 , 214 / 255. , 96  / 255. , 77  / 255.))
mycolors.append(r.TColor(11002 , 244 / 255. , 165 / 255. , 130 / 255.))
mycolors.append(r.TColor(11001 , 253 / 255. , 219 / 255. , 199 / 255.))
mycolors.append(r.TColor(11000 , 247 / 255. , 247 / 255. , 247 / 255.))
mycolors.append(r.TColor(11011 , 209 / 255. , 229 / 255. , 240 / 255.))
mycolors.append(r.TColor(11012 , 146 / 255. , 197 / 255. , 222 / 255.))
mycolors.append(r.TColor(11013 , 67  / 255. , 147 / 255. , 195 / 255.))
mycolors.append(r.TColor(11014 , 33  / 255. , 102 / 255. , 172 / 255.))
mycolors.append(r.TColor(11015 , 5   / 255. , 48  / 255. , 97  / 255.))

mycolors.append(r.TColor(3001 , 239 / 255. , 138 / 255. , 98  / 255.))
mycolors.append(r.TColor(3000 , 247 / 255. , 247 / 255. , 247 / 255.))
mycolors.append(r.TColor(3011 , 103 / 255. , 169 / 255. , 207 / 255.))

mycolors.append(r.TColor(5001 , 251 / 255. , 180 / 255. , 174 / 255.))
mycolors.append(r.TColor(5002 , 179 / 255. , 205 / 255. , 227 / 255.))
mycolors.append(r.TColor(5003 , 204 / 255. , 235 / 255. , 197 / 255.))
mycolors.append(r.TColor(5004 , 222 / 255. , 203 / 255. , 228 / 255.))
mycolors.append(r.TColor(5005 , 254 / 255. , 217 / 255. , 166 / 255.))

mycolors.append(r.TColor(7000 ,   0/255. ,   0/255. ,   0/255.))
mycolors.append(r.TColor(7001 , 213/255. ,  94/255. ,   0/255.)) #r
mycolors.append(r.TColor(7002 , 230/255. , 159/255. ,   0/255.)) #o
mycolors.append(r.TColor(7003 , 240/255. , 228/255. ,  66/255.)) #y
mycolors.append(r.TColor(7004 ,   0/255. , 158/255. , 115/255.)) #g
mycolors.append(r.TColor(7005 ,   0/255. , 114/255. , 178/255.)) #b
mycolors.append(r.TColor(7006 ,  86/255. , 180/255. , 233/255.)) #k
mycolors.append(r.TColor(7007 , 204/255. , 121/255. , 167/255.)) #p
mycolors.append(r.TColor(7011 , 110/255. ,  54/255. ,   0/255.)) #alt r
mycolors.append(r.TColor(7012 , 161/255. , 117/255. ,   0/255.)) #alt o
mycolors.append(r.TColor(7013 , 163/255. , 155/255. ,  47/255.)) #alt y
mycolors.append(r.TColor(7014 ,   0/255. , 102/255. ,  79/255.)) #alt g
mycolors.append(r.TColor(7015 ,   0/255. ,  93/255. , 135/255.)) #alt b
mycolors.append(r.TColor(7016 , 153/255. , 153/255. , 153/255.)) #alt k
mycolors.append(r.TColor(7017 , 140/255. ,  93/255. , 119/255.)) #alt p

mycolors.append(r.TColor(9001 ,  60/255. , 186/255. ,  84/255.))
mycolors.append(r.TColor(9002 , 244/255. , 194/255. ,  13/255.))
mycolors.append(r.TColor(9003 , 219/255. ,  50/255. ,  54/255.))
mycolors.append(r.TColor(9004 ,  72/255. , 133/255. , 237/255.))

# Color schemes from Hannsjoerg for WWW analysis
mycolors.append(r.TColor(2001 , 91  / 255. , 187 / 255. , 241 / 255.)) #light-blue
mycolors.append(r.TColor(2002 , 60  / 255. , 144 / 255. , 196 / 255.)) #blue
mycolors.append(r.TColor(2003 , 230 / 255. , 159 / 255. , 0   / 255.)) #orange
mycolors.append(r.TColor(2004 , 180 / 255. , 117 / 255. , 0   / 255.)) #brown
mycolors.append(r.TColor(2005 , 245 / 255. , 236 / 255. , 69  / 255.)) #yellow
mycolors.append(r.TColor(2006 , 215 / 255. , 200 / 255. , 0   / 255.)) #dark yellow
mycolors.append(r.TColor(2007 , 70  / 255. , 109 / 255. , 171 / 255.)) #blue-violet
mycolors.append(r.TColor(2008 , 70  / 255. , 90  / 255. , 134 / 255.)) #violet
mycolors.append(r.TColor(2009 , 55  / 255. , 65  / 255. , 100 / 255.)) #dark violet
mycolors.append(r.TColor(2010 , 120 / 255. , 160 / 255. , 0   / 255.)) #light green
mycolors.append(r.TColor(2011 , 0   / 255. , 158 / 255. , 115 / 255.)) #green
mycolors.append(r.TColor(2012 , 204 / 255. , 121 / 255. , 167 / 255.)) #pink?

class HistData:
    """
    HistData class to hold the histograms I need.
    """
    def __init__(self):
        self.nom = None
        self.systs = []
        self.upsysts = []
        self.downsysts = []
        self.normsysts = []
        self.totalerr = None

def cloneTH1(obj, name=""):
    """
    Clone any TH1 object with the same name or new name.
    """
    if name == "":
        name = obj.GetName()
    rtn = obj.Clone(name)
    rtn.SetTitle("")
    if not rtn.GetSumw2N():
        rtn.Sumw2()
    rtn.SetDirectory(0)
    return rtn;

def getTotalErrByMaxDiff(nom, systs):
    """
    Given a nominal histogram and list of systematics,
    returns a single histogram that takes the maximum
    variation from the list of systs. The returned
    histogram has nominal value + difference in each
    bin.
    """
    err = cloneTH1(nom)
    rtn = cloneTH1(nom)
    err.Reset()
    for syst in systs:
        for ibin in xrange(0, syst.GetNbinsX()+2):
            systcontent = syst.GetBinContent(ibin)
            nomicontent = nom.GetBinContent(ibin)
            thisdiff = abs(systcontent - nomicontent)
            currmaxdiff = err.GetBinContent(ibin)
            if currmaxdiff < thisdiff:
                err.SetBinContent(ibin, thisdiff)
                rtn.SetBinContent(ibin, thisdiff + nomicontent)
    return rtn

def getTotalErrBySqSum(nom, systs, normfracsyst=0):
    """
    Given a nominal histogram and list of systematics
    (optional: plus a single fractional normalization
    systematics), returns a single histogram that has
    the total uncertainty (in absolute value) on each bin.
    """
    if nom:
        err = cloneTH1(nom)
    else:
        try:
            err = cloneTH1(systs[0])
        except:
            print "ERROR - Neither nominal nor systematic histograms are provided"
    err.Reset()
    if nom:
        for ibin in xrange(0, nom.GetNbinsX()+2):
            err.SetBinContent(ibin, nom.GetBinError(ibin))
    for syst in systs:
        for ibin in xrange(0, syst.GetNbinsX()+2):
            systcontent = syst.GetBinContent(ibin)
            nomicontent = 0
            if nom:
                nomicontent = nom.GetBinContent(ibin)
            thiserr = abs(systcontent - nomicontent)
            currerr = err.GetBinContent(ibin)
            thiserr = math.sqrt(thiserr ** 2 + currerr ** 2)
            err.SetBinContent(ibin, thiserr)
    if normfracsyst > 0:
        for ibin in xrange(0, syst.GetNbinsX()+2):
            currerr = err.GetBinContent(ibin)
            nomicontent = nom.GetBinContent(ibin)
            normsyst = nomicontent * normfracsyst
            thiserr = math.sqrt(normsyst ** 2 + currerr ** 2)
            err.SetBinContent(ibin, thiserr)
    return err

def getTotalErrFromSystLists(nom, upsysts, dnsysts, normfracsyst=0):
    """
    Combine two lists of up and down variations into
    a single error systematics histogram
    """
    if len(upsysts) != len(dnsysts):
        print "ERROR - the number of up and down systematic variations do not match."
        sys.exit()
    systs = []
    for pair in zip(upsysts, dnsysts):
        systs.append(getTotalErrByMaxDiff(nom, [pair[0], pair[1]]))
    return getTotalErrBySqSum(nom, systs, normfracsyst)

def getTotalBkgHist(hists):
    """
    Sum all histograms and return a new copy of total bkg hist.
    """
    if len(hists) == 0:
        print "ERROR - the number of histograms are zero, while you asked me to sum them up."
    totalhist = cloneTH1(hists[0])
    totalhist.Reset()
    for hist in hists:
        totalhist.Add(hist)
    return totalhist

def makeHistDataFromTH2(th2, dosyst=True, options={}):
    """
    Creates an instance of "HistData" class from a single TH2.
    I use TH2's to represent a single process histograms.
    TH2's y-bin-index = 1 is the nominal histogram
    TH2's y-bin-index > 1 are are the systematic histograms. (Absolute values not fractional or difference.)
    TH2's even y-bin-index are the up variations.
    TH2's odd y-bin-index are the down variations.
    TH2's 0, 0 is the overall norm systematics.
    """
    if not th2:
        return HistData()
    hist = HistData()
    for ibin in xrange(1, th2.GetNbinsY() + 1):
        if not dosyst:
            if ibin > 1:
                break
        name = th2.GetName()
        # https://root-forum.cern.ch/t/setbinlabel-causes-unexpected-behavior-when-handling-the-histograms/26202/2
        labels = th2.GetXaxis().GetLabels()
        if labels:
            th2.GetXaxis().SetRange(1, th2.GetXaxis().GetNbins())
        if ibin != 1:
            name += "syst{}".format(ibin - 1)
        projhist = th2.ProjectionX("{}".format(uuid.uuid4()), ibin, ibin)
        projhist.SetName(name)
        projhist.SetDirectory(0)
        if "nbin" in options:
            currnbin = projhist.GetNbinsX()
            frac = currnbin / options["nbin"]
            projhist.Rebin(frac)
        if ibin == 1:
            hist.nom = projhist
        else:
            if ibin % 2 == 0:
                hist.upsysts.append(projhist)
            else:
                hist.downsysts.append(projhist)
    hist.normsysts.append(th2.GetBinContent(0, 0))
    if dosyst:
        hist.totalerr = getTotalErrFromSystLists(hist.nom, hist.upsysts, hist.downsysts, hist.normsysts[0])
    else:
        hist.totalerr = cloneTH1(hist.nom)
    return hist

def makeHistDatasFromTH2s(th2s, options={}):
    """
    From a list of TH2s, return a list of nominal
    histograms and a list of error histograms.
    """
    noms = []
    errs = []
    for th2 in th2s:
        hist = makeHistDataFromTH2(th2, options=options)
        noms.append(hist.nom)
        errs.append(hist.totalerr)
    totalerr = getTotalErrBySqSum(getTotalBkgHist(noms), errs)
    return noms, errs

def makeBkgHistDatasFromTH2s(th2s, options={}):
    """
    From a list of TH2s, return a list of nominal
    bkg histograms and a single combined total error histograms.
    """
    noms, errs = makeHistDatasFromTH2s(th2s, options)
    totalerr = getTotalErrBySqSum(None, errs)
    return noms, totalerr

def getYaxisRange(hist):
    maximum = 0
    if hist:
        for ibin in xrange(1, hist.GetNbinsX()+1):
            c = hist.GetBinContent(ibin)
            e = hist.GetBinError(ibin)
            v = c + e
            if v > maximum:
                maximum = v

    return maximum

def getMaxYaxisRange(hists):
    maximum = 0
    for hist in hists:
        v = getYaxisRange(hist)
        if v > maximum:
            maximum = v
    return maximum

def rebin(hists, nbin):
    for hist in hists:
        if not hist: continue
        currnbin = hist.GetNbinsX()
        fac = currnbin / nbin
        hist.Rebin(fac)

def removeErrors(hists):
    for hist in hists:
        for ibin in xrange(0, hist.GetNbinsX()+2):
            hist.SetBinError(ibin, 0)

def plot_hist(th2_data, th2s_bkg, th2s_sig, options, colors=[], sig_labels=[], legend_labels=[]):
    """
    Plot 1d plot based off of th2s
    bkg histograms and a single combined total error histograms.
    Some operations are additionally done.
    """
    hdata = makeHistDataFromTH2(th2_data, False, options=options).nom
    hbgs, hsyst = makeBkgHistDatasFromTH2s(th2s_bkg, options=options)
    hsigs, hsigerrs = makeHistDatasFromTH2s(th2s_sig, options=options)
    # Rebinning occurs during "makeHist" delete the option afterwards
    if "nbin" in options: del options["nbin"]
    hsig_labels = []
    if len(sig_labels) == 0:
        for hsig in hsigs:
            hsig_labels.append(hsig.GetName())
    hcolors = colors
    if len(colors) == 0:
        for index, hbg in enumerate(hbgs):
            hcolors.append(2001 + index)
    hlegend_labels = []
    if len(legend_labels) == 0:
        for hbg in hbgs:
            hlegend_labels.append(hbg.GetName())
    # If hsyst has integral of 0 remove it
    if hsyst.Integral() == 0:
        hsyst = None
    # Setting maximums
    totalbkg = getTotalBkgHist(hbgs)
    yaxismax = getMaxYaxisRange([hdata, totalbkg]) * 1.8
    removeErrors(hbgs)
    if yaxismax < 100:
        options["yaxis_title_offset"] = 1.2
    elif yaxismax < 1000:
        options["yaxis_title_offset"] = 1.45
    elif yaxismax < 10000:
        options["yaxis_title_offset"] = 1.6
    else:
        options["yaxis_title_offset"] = 1.8
    if not "canvas_width"             in options: options["canvas_width"]              = 604
    if not "canvas_height"            in options: options["canvas_height"]             = 728
    if not "yaxis_range"              in options: options["yaxis_range"]               = [0., yaxismax]
    if not "legend_ncolumns"          in options: options["legend_ncolumns"]           = 2
    if not "legend_alignment"         in options: options["legend_alignment"]          = "topright"
    if not "legend_smart"             in options: options["legend_smart"]              = True
    if not "legend_scalex"            in options: options["legend_scalex"]             = 1.4
    if not "legend_scaley"            in options: options["legend_scaley"]             = 1.4
    if not "legend_border"            in options: options["legend_border"]             = False
    if not "legend_percentageinbox"   in options: options["legend_percentageinbox"]    = False
    if not "hist_line_none"           in options: options["hist_line_none"]            = True
    if not "show_bkg_errors"          in options: options["show_bkg_errors"]           = False
    if not "ratio_range"              in options: options["ratio_range"]               = [0.7, 1.3]
    if not "ratio_name_size"          in options: options["ratio_name_size"]           = 0.13
    if not "ratio_name_offset"        in options: options["ratio_name_offset"]         = 0.6
    if not "ratio_xaxis_label_offset" in options: options["ratio_xaxis_label_offset"]  = 0.06
    if not "ratio_yaxis_label_offset" in options: options["ratio_yaxis_label_offset"]  = 0.03
    if not "ratio_xaxis_title_offset" in options: options["ratio_xaxis_title_offset"]  = 1.40
    if not "ratio_xaxis_title_size"   in options: options["ratio_xaxis_title_size"]    = 0.13
    if not "ratio_label_size"         in options: options["ratio_label_size"]          = 0.13
    if not "canvas_tick_one_side"     in options: options["canvas_tick_one_side"]      = True
    if not "canvas_main_y1"           in options: options["canvas_main_y1"]            = 0.2
    if not "canvas_main_topmargin"    in options: options["canvas_main_topmargin"]     = 0.2 / 0.7 - 0.2
    if not "canvas_main_rightmargin"  in options: options["canvas_main_rightmargin"]   = 50. / 600.
    if not "canvas_main_bottommargin" in options: options["canvas_main_bottommargin"]  = 0.2
    if not "canvas_main_leftmargin"   in options: options["canvas_main_leftmargin"]    = 130. / 600.
    if not "canvas_ratio_y2"          in options: options["canvas_ratio_y2"]           = 0.342
    if not "canvas_ratio_topmargin"   in options: options["canvas_ratio_topmargin"]    = 0.05
    if not "canvas_ratio_rightmargin" in options: options["canvas_ratio_rightmargin"]  = 50. / 600.
    if not "canvas_ratio_bottommargin"in options: options["canvas_ratio_bottommargin"] = 0.4
    if not "canvas_ratio_leftmargin"  in options: options["canvas_ratio_leftmargin"]   = 130. / 600.
    if not "xaxis_title_size"         in options: options["xaxis_title_size"]          = 0.06
    if not "yaxis_title_size"         in options: options["yaxis_title_size"]          = 0.06
    if not "xaxis_label_size_scale"   in options: options["xaxis_label_size_scale"]    = 1.4
    if not "yaxis_label_size_scale"   in options: options["yaxis_label_size_scale"]    = 1.4
    if not "xaxis_label_offset_scale" in options: options["xaxis_label_offset_scale"]  = 4.0
    if not "yaxis_label_offset_scale" in options: options["yaxis_label_offset_scale"]  = 4.0
    if not "xaxis_tick_length_scale"  in options: options["xaxis_tick_length_scale"]   = -0.8
    if not "yaxis_tick_length_scale"  in options: options["yaxis_tick_length_scale"]   = -0.8
    if not "ratio_tick_length_scale"  in options: options["ratio_tick_length_scale"]   = -1.0
    if not "output_name"              in options: options["output_name"]               = "plot.png"
    if not "cms_label"                in options: options["cms_label"]                 = "Preliminary"
    if not "lumi_value"               in options: options["lumi_value"]                = "35.9"
    if not "bkg_err_fill_style"       in options: options["bkg_err_fill_style"]        = 3245
    if not "bkg_err_fill_color"       in options: options["bkg_err_fill_color"]        = 1
    p.plot_hist(
            data          = hdata,
            bgs           = hbgs,
            sigs          = hsigs,
            syst          = hsyst,
            sig_labels    = hsig_labels,
            colors        = hcolors,
            legend_labels = hlegend_labels,
            options       = options
            )
