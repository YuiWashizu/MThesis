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
 
def EnablePixel(filename, collistw, collistwo, totw, totwo, tot3w, tot3wo, tot4w, tot4wo, totwnom, totwonom):
    f = open(filename, 'r')
    json_data = json.load(f)
    
    trigw = 1000./4056311.
    trigwo = 1000./4193686.

    print(type(trigw))
    print(type(trigwo))

    for col in range(264, 400):
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in range(0, 192):
            if colnum["Enable"][int(row)] == 1:
                nhitsw = len(collistw[col][row])
                nhitswo = len(collistwo[col][row])
                if nhitsw != 0:
                    if nhitswo == 0:

                        #with source
                        for itot in collistw[col][row]:
                            totw.Fill(itot)
                            totwnom.Fill(itot, trigw)
                            tot3w.Fill(itot, trigw)
                        #without source
                        for itotwo in collistwo[col][row]:
                            totwo.Fill(itotwo)
                            totwnom.Fill(itotwo, trigwo)
                            tot3wo.Fill(itotwo, trigwo)
#                            if itot >= 3:
#                                switch = 1
#                        if switch == 1:
#                            nhits3than5 += 1
#                            hit3than5.Fill(nhitsw)
                    else:
                        #with source
                        for itot in collistw[col][row]:
                            totw.Fill(itot)
                            totwnom.Fill(itot, trigw)
                            tot4w.Fill(itot, trigw)
                        #without source
                        for itotwo in collistwo[col][row]:
                            totwo.Fill(itotwo)
                            totwonom.Fill(itotwo, trigwo)
                            tot4wo.Fill(itotwo, trigwo)


def main():
    args = sys.argv
    ws = args[1]
    wos = args[2]
    fileEn = "./data/015902_std_exttrigger_KEK53-4/rd53a_test.json.before"
    outputw = ROOT.TFile(ws + "_ToT.root", 'RECREATE')
    outputwo = ROOT.TFile(wos + "_ToT.root", 'RECREATE')
    
    collistw = {}
    collistwo = {}
    ReadRootfile(ws, collistw)
    ReadRootfile(wos, collistwo)

    #define histogram
    totw = TH1F("tot", "", 16, 0, 16)
    totwo = TH1F("tot", "", 16, 0, 16)
    tot3w = TH1F("tot3", "", 16, 0, 16)
    tot3wo = TH1F("tot3", "", 16, 0, 16)
    tot4w = TH1F("tot4", "", 16, 0, 16)
    tot4wo = TH1F("tot4", "", 16, 0, 16)
    totwnom = TH1F("totnom", "", 16, 0, 16)
    totwonom = TH1F("totnom", "", 16, 0, 16)

    EnablePixel(fileEn, collistw, collistwo, totw, totwo, tot3w, tot3wo, tot4w, tot4wo, totwnom, totwonom)

    outputw.cd()
    totw.Write()
    tot3w.Write()
    tot4w.Write()
    totwnom.Write()
    outputw.Close()

    outputwo.cd()
    totwo.Write()
    tot3wo.Write()
    tot4wo.Write()
    totwonom.Write()
    outputwo.Close()

        
if __name__=='__main__':
    main()
