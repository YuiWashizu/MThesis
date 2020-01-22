#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TF1, TH1F, TH2F, TGraph, gStyle, TCanvas
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
from array import array

def ReadRootfile(filename, collist):
    file = ROOT.TFile(filename, 'READ')
    tree = file.Get('extree')
    nevents = tree.GetEntries()
    print("nevents : {}".format(nevents))
    rowlist = []
    for ievent in range(nevents):
        tree.GetEntry(ievent)
        ntot = tree.hit_tot.size()
        totlist = []
        for itot in range(ntot):
            totlist.append(tree.hit_tot[itot])
        rowlist.append(totlist)
        if (ievent%192 == 191):
            collist[math.floor(ievent/192)] = rowlist
            rowlist = []
 
def EnablePixel(filename, collistw, collistwo):
    f = open(filename, 'r')
    json_data = json.load(f)

    trigw = 4056311
    trigwo = 4193686
    
    nhits3 = 0
    nhits3dbg = 0
    nhits4 = 0
    pixel3 = 0
    pixel3dbg = 0
    pixel4 = 0
    pixel4dbg = 0

    for col in range(264, 400):
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in range(0, 192):
            if colnum["Enable"][int(row)] == 1:
                nhitsw = len(collistw[col][row])
                nhitswo = len(collistwo[col][row])
                if nhitsw != 0:
                    #patern 3
                    if nhitswo == 0:
                        if nhitsw > 2:
                            nhits3 = nhits3 + nhitsw
                            pixel3 += 1
                        else:
                            pixel3dbg += 1
                    #patern 4
                    else:
                        n = 0.
                        nbg = 0.
                        nsigratio = 0.
                        for itot in collistw[col][row]:
                            if itot > 5:
                                n += 1
                        for itot in collistwo[col][row]:
                            if itot > 5:
                                nbg += 1
                        nsig = n/trigw - nbg/trigwo
                        sigma = np.sqrt(nbg/trigwo)
                        if nsig/sigma > 5.:
                            print("n    : {}".format(n))
                            print("nbg  : {}".format(nbg))
                            print("nsig : {}".format(nsig))
                            nsigratio = nsig/(n/trigw)
                            nhits4 = nhits4 + n*nsigratio
                            pixel4 += 1
                        else:
                            pixel4dbg += 1

    print("nhits3    : {}".format(nhits3))
    print("nhits4    : {}".format(nhits4))
    print("pixel3    : {}".format(pixel3))
    print("pixel3dbg : {}".format(pixel3dbg)) 
    print("pixel4    : {}".format(pixel4))
    print("pixel4dbg : {}".format(pixel4dbg))



def main():
    args = sys.argv
    ws = args[1]
    wos = args[2]
    fileEn = "./data/015902_std_exttrigger_KEK53-4/rd53a_test.json.before"
    outputw = ROOT.TFile(ws + "_Ana.root", 'RECREATE')
    outputwo = ROOT.TFile(wos + "_Ana.root", 'RECREATE')
    
    collistw = {}
    collistwo = {}
    ReadRootfile(ws, collistw)
    ReadRootfile(wos, collistwo)


    EnablePixel(fileEn, collistw, collistwo)

        
if __name__=='__main__':
    main()
