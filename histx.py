#!/bin/env python

#
# HistX
#

#  .
# ..: P.Chang, philip@physics.ucsd.edu

import ROOT as r
import math
import sys
import uuid
import os
sys.path.append("{0}/syncfiles/pyfiles".format(os.path.realpath(__file__).rsplit("/",1)[0]))
from pytable import *
from errors import E

class HistX:
    """

    ===========
    HistX class
    ===========

        I use TH2's to represent a single process histogram.
        TH2's y-bin-index = 1 is the nominal histogram
        TH2's y-bin-index > 1 are are the systematic histograms. (Absolute values not fractional or difference.)
        TH2's even y-bin-index are the up variations.
        TH2's odd y-bin-index are the down variations.
        (if only the even y-bin-index is filled, with corresponding odd one set empty, take the odd as symmetric.)
        TH2's 0, 0 is the overall norm systematics. (If only this is set)
        TH2's N+1, N+1 is the overall upward norm systematics.(If both 0,0 and N+1,N+1 is set)

        When plotting, there are two ways to retrieve a histogram.
            1. Single TH1, with an error set to SumSq of max deviation taken from each pair of up/down systematics.
            2. Nominal TH1, with an error set to stat error only plus two error histograms.
               (First error histogram's content set to sum sq of all +errors and vice versa on the second.)

    """

    #_____________________________________________________________________________________________
    def __init__(self, th2, options={}):
        self.th2 = th2
        self.options = options
        self.nom = None
        self.up_systs = []
        self.dn_systs = []
        self.sym_total_err = None
        self.nom_plus_sym_total_error = None
        self.up_error = None
        self.dn_error = None
        self.process()

    #_____________________________________________________________________________________________
    def get_hist(self):
        return self.nom_plus_sym_total_error

    #_____________________________________________________________________________________________
    def get_hist_no_syst(self):
        return self.nom

    #_____________________________________________________________________________________________
    def get_hist_with_asym_err(self):
        return self.nom, self.up_error, self.dn_error

    #_____________________________________________________________________________________________
    def process(self):
        self.deconstruct_TH2s_to_list_of_TH1s()
        self.aggregate_TH1s()

    #_____________________________________________________________________________________________
    def deconstruct_TH2s_to_list_of_TH1s(self):
        """
        Goal: set the following
            self.nom
            self.up_systs
            self.dn_systs
        """
        # Sanity check
        if not self.th2:
            print "[HistX] >>> Warning! I received a null TH2!"
            return
        nbin = self.th2.GetNbinsX()
        nsyst = self.th2.GetNbinsY()
        histname = self.th2.GetName()
        # Loop over the Y-direction of the TH2, which signifies the systematic variations.
        for ibin in xrange(1, nsyst + 1):
            # Weird behavior in ROOT. Read the function definition.
            self.safe_guard_bin_labels()
            # Get the name of the histogram
            name = histname
            # If not nominal sample modify the name
            if ibin != 1: name += "_syst{}".format(ibin - 1)
            # Create a 1D histogram from a given y-axis line
            projhist = self.th2.ProjectionX(self.unique_id(), ibin, ibin)
            projhist.SetName(name)
            projhist.SetDirectory(0)
            # If needed to be rebinned, rebin
            self.rebin(projhist)
            if ibin == 1:
                self.nom = projhist
            else:
                if ibin % 2 == 0:
                    self.up_systs.append(projhist)
                else:
                    # If the integral = 0 then add the one added to the up_systs
                    if projhist.Integral() == 0:
                        self.dn_systs.append(self.cloneTH1(self.up_systs[-1], histname + "_syst{}".format(ibin - 1)))
                    else:
                        self.dn_systs.append(projhist)
        # Take care of per bin normalization systematics
        fracuperrs = []
        fracdnerrs = []
        for ibin in xrange(1, nbin + 1):
            ifracuperr = self.th2.GetBinContent(ibin, 0)
            ifracdnerr = self.th2.GetBinContent(ibin, nsyst + 1)
            fracuperrs.append(ifracuperr)
            fracdnerrs.append(ifracdnerr)
        # Check whether all of the dn variations are 0
        if all(e == 0 for e in fracuperrs): fracuperrs = [0] * len(fracuperrs)
        if all(e == 0 for e in fracdnerrs): fracdnerrs = fracuperrs
        hist_up_norm_per_bin_syst = self.cloneTH1(self.nom, histname + "_up_norm_per_bin")
        hist_dn_norm_per_bin_syst = self.cloneTH1(self.nom, histname + "_dn_norm_per_bin")
        for index, (upfe, dnfe) in enumerate(zip(fracuperrs, fracdnerrs)):
            ibin = index + 1
            nom = hist_up_norm_per_bin_syst.GetBinContent(ibin)
            newuperr = upfe * nom
            newdnerr = dnfe * nom
            hist_up_norm_per_bin_syst.SetBinContent(ibin, nom + newuperr)
            hist_dn_norm_per_bin_syst.SetBinContent(ibin, nom - newdnerr)
        self.up_systs.append(hist_up_norm_per_bin_syst)
        self.dn_systs.append(hist_dn_norm_per_bin_syst)
        # Take care of flat normalization systematics
        up_norm_syst = self.th2.GetBinContent(0, 0)
        dn_norm_syst = self.th2.GetBinContent(nbin + 1, nsyst + 1)
        if up_norm_syst == 0: return
        if dn_norm_syst == 0: dn_norm_syst = up_norm_syst
        hist_up_norm_syst = self.cloneTH1(self.nom, histname + "_up_norm")
        hist_dn_norm_syst = self.cloneTH1(self.nom, histname + "_dn_norm")
        hist_up_norm_syst.Scale(1 + up_norm_syst)
        hist_dn_norm_syst.Scale(1 - dn_norm_syst)
        self.up_systs.append(hist_up_norm_syst)
        self.dn_systs.append(hist_dn_norm_syst)
        return

    #_____________________________________________________________________________________________
    def aggregate_TH1s(self):
        """
        Goal: set the following
            self.sym_total_err
            self.nom_plus_sym_total_error
            self.up_error
            self.dn_error
        """
        self.process_nom_plus_sym_total_err()
        self.process_up_dn_error()

    #_____________________________________________________________________________________________
    def process_nom_plus_sym_total_err(self):
        """
        Goal: set the following
            self.sym_total_err
            self.nom_plus_sym_total_error
        """
        self.compute_symmetric_total_err()
        self.make_nom_plus_sym_total_err()

    #_____________________________________________________________________________________________
    def process_up_dn_error(self):
        """
        Goal: set the following
            self.up_error
            self.dn_error
        """
        up_errs = []
        dn_errs = []
        for pair in zip(self.up_systs, self.dn_systs):
            up_err, dn_err = self.get_asym_err_from_syst_pair(pair)
            up_errs.append(up_err)
            dn_errs.append(dn_err)
        self.up_error = self.get_total_err_by_sqsum(up_errs)
        self.dn_error = self.get_total_err_by_sqsum(dn_errs)

    #_____________________________________________________________________________________________
    def compute_symmetric_total_err(self):
        """
        Goal: set the following
            self.sym_total_err
        """
        errs = []
        for pair in zip(self.up_systs, self.dn_systs):
            errs.append(self.get_sym_err_from_syst_pair(pair))
        self.sym_total_err = self.get_total_err_by_sqsum(errs)

    #_____________________________________________________________________________________________
    def make_nom_plus_sym_total_err(self):
        """
        Goal: set the following
            self.nom_plus_sym_total_error
        """
        self.nom_plus_sym_total_error = self.cloneTH1(self.nom)
        for i in xrange(0, self.nom_plus_sym_total_error.GetNbinsX() + 2):
            nom_err = self.nom_plus_sym_total_error.GetBinError(i)
            sym_err = self.sym_total_err.GetBinContent(i)
            new_err = math.sqrt(nom_err**2 + sym_err**2)
            self.nom_plus_sym_total_error.SetBinError(i, new_err)

    #_____________________________________________________________________________________________
    def get_sym_err_from_syst_pair(self, pair):
        """
        from a pair of systematic,
        returns a single histogram that takes the maximum
        variation from the list of systs. The returned
        histogram has the difference.
        bin.
        """
        err = self.cloneTH1(self.nom)
        err.Reset()
        for syst in pair:
            for ibin in xrange(0, syst.GetNbinsX() + 2):
                systcontent = syst.GetBinContent(ibin)
                nomicontent = self.nom.GetBinContent(ibin)
                thisdiff = abs(systcontent - nomicontent)
                currmaxdiff = err.GetBinContent(ibin)
                if currmaxdiff < thisdiff:
                    err.SetBinContent(ibin, thisdiff)
        return err

    #_____________________________________________________________________________________________
    def get_asym_err_from_syst_pair(self, pair):
        """
        from a pair of systematic,
        returns a single histogram that takes the maximum
        variation from the list of systs but only in upward/downward error.
        """
        up_err = self.cloneTH1(self.nom)
        up_err.Reset()
        dn_err = self.cloneTH1(self.nom)
        dn_err.Reset()
        for syst in pair:
            for ibin in xrange(0, syst.GetNbinsX() + 2):
                systcontent = syst.GetBinContent(ibin)
                nomicontent = self.nom.GetBinContent(ibin)
                thisdiff = systcontent - nomicontent
                if thisdiff > 0:
                    currmaxdiff = up_err.GetBinContent(ibin)
                    if currmaxdiff < abs(thisdiff):
                        up_err.SetBinContent(ibin, abs(thisdiff))
                else:
                    currmaxdiff = dn_err.GetBinContent(ibin)
                    if currmaxdiff < abs(thisdiff):
                        dn_err.SetBinContent(ibin, abs(thisdiff))
        return up_err, dn_err

    #_____________________________________________________________________________________________
    def get_total_err_by_sqsum(self, errs):
        """
        Given a list of TH1s of errs, sumsq the contents
        """
        total_err = None
        for err in errs:
            if not total_err:
                total_err = self.cloneTH1(err)
                total_err.Reset()
            for i in xrange(0, err.GetNbinsX() + 2):
                curr_tot_err = total_err.GetBinContent(i)
                this_err = err.GetBinContent(i)
                new_tot_err = math.sqrt(curr_tot_err**2 + this_err**2)
                total_err.SetBinContent(i, new_tot_err)
        return total_err

    #_____________________________________________________________________________________________
    def cloneTH1(self, obj, name=""):
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
        # https://root-forum.cern.ch/t/setbinlabel-causes-unexpected-behavior-when-handling-the-histograms/26202/2
        labels = rtn.GetXaxis().GetLabels()
        if labels:
            rtn.GetXaxis().SetRange(1, rtn.GetXaxis().GetNbins())
        return rtn;


    #_____________________________________________________________________________________________
    def unique_id(self):
        return "{}".format(uuid.uuid4())

    #_____________________________________________________________________________________________
    def safe_guard_bin_labels(self):
        # https://root-forum.cern.ch/t/setbinlabel-causes-unexpected-behavior-when-handling-the-histograms/26202/2
        labels = self.th2.GetXaxis().GetLabels()
        if labels:
            self.th2.GetXaxis().SetRange(1, self.th2.GetXaxis().GetNbins())

    #_____________________________________________________________________________________________
    def rebin(self, projhist):
        if "nbin" in self.options:
            currnbin = projhist.GetNbinsX()
            frac = currnbin / self.options["nbin"]
            projhist.Rebin(frac)

