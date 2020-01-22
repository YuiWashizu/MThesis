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

def ReadJsonfile(filename, hist):
    file = open(filename, 'r')
    for line in file.readlines()[8:]:
        itemList = line.split(' ')
        numbers = []
        #print(itemList)
        for item in itemList:
            if item == '\n':
                #print('enter end')
                break
                #print(int(item))
            numbers.append(float(item))
        hist.append(numbers)

def ReadRootfile(filename, collist):
    file = ROOT.TFile(filename, 'READ')
    tree = file.Get('extree')
    nevents = tree.GetEntries()
    print("nevents : {}".format(nevents))
    rowlist = []
    for ievent in range(50688, nevents): #26112
        tree.GetEntry(ievent)
        ntot = tree.hit_tot.size()
        totlist = []
        for itot in range(ntot):
            totlist.append(tree.hit_tot[itot])
        rowlist.append(totlist)
        if (ievent%192 == 191):
            collist[math.floor(ievent/192)] = rowlist
            rowlist = []

def EnablePixel(fileEn, noiselist, collistw, collistwo, h_rrandom, h_nw, h_nsig, h_nsigfit, h_nsigfitzoom, h_wsig, h_nsigmap, trigger, triggerw):
    f = open(fileEn, 'r')
    json_data = json.load(f)
    
    trigw = 918246
    trigwo = 29353
    
    nhits3 = 0
    nhits3dbg = 0
    nhits4 = 0
    pixel3 = 0
    pixel3dbg = 0
    pixel4 = 0
    pixel4dbg = 0

    Nsig = 0
    Nemp = 0
    Nall = 0
    nsigcount = 0
    zerosigcount = 0

    for col in range(264, 400):
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in range(0, 192):
            if colnum["Enable"][int(row)] == 1:
                nrandom = noiselist[row][col] # N_random
                rrandom = float(nrandom)/float(trigger) # R_random
                nw = len(collistw[col][row]) # N_w
                rw = float(nw) / float(triggerw) # R_w
                nsig = int(nw) - int(float(rrandom)*float(triggerw))
                
                if nsig < 0:
                    nsig = 0

                if nw == 0:
                    Nemp += 1
                else:
                    Nall = Nall + nw
                if nsig != 0:
                    Nsig = Nsig + nsig
                    nsigcount += 1
                else:
                    zerosigcount += 1

                h_rrandom.Fill(rrandom)
                h_nw.Fill(nw)
                h_nsig.Fill(nsig)
                h_nsigfit.Fill(nsig)
                h_nsigfitzoom.Fill(nsig)
                h_nsigmap.SetBinContent(h_nsigmap.GetBin(col-264, row), nsig)

                nw = nw + 1
                nsig = nsig + 1
                h_wsig.Fill(nw, nsig)

    print("Nsig         : {}".format(Nsig))
    print("Nemp         : {}".format(Nemp))
    print("Nall         : {}".format(Nall))
    print("nsigcount    : {}".format(nsigcount))
    print("zerosigcount : {}".format(zerosigcount))

def FitPoisson(hist, hitmin, hitmax, mean):
    poisson = TF1('poisson', '[0]*TMath::Poisson(x,[1])', hitmin, hitmax)
    poisson.SetParameter(0, 50000)
    poisson.SetParameter(1, mean)
    hist.Fit("poisson", "", "", hitmin, hitmax)
    slope0 = poisson.GetParameter(0)
    mean0 = poisson.GetParameter(1)

    print("mean0 : {}".format(mean0))


def main():
    args = sys.argv
    ws = args[1]
    fileNoise = "./data/015894_std_noisescan_KEK53-4/JohnDoe_Occupancy.dat"
    fileEn = "./data/015902_std_exttrigger_KEK53-4/rd53a_test.json.before"

    output = ROOT.TFile("ExtAna.root", 'RECREATE')
    trigger = 200000 * 300
    triggerw = int((14872830 + 11378452 + 9962243)/16)

    bina = [0., 0.5]
    binb = range(1, 10001)
    bindef = bina + binb
    numbin = int(len(bindef) - 1)

    h_rrandom = TH1F("rrandom", "", trigger, 0, 1)
    h_nw = TH1F("nhitsw", "", 100000, 0, 100000)
    h_nsig = TH1F("nhitsw", "", 100000, 0, 100000)
    h_nsigfit = TH1F("nsigfit", "", 100000, 0, 100000) 
    h_nsigfitzoom = TH1F("nsigfitzoom", "", 15, 0, 15) 
    h_wsig = TH2F("NwVSNsig", "", 10000, 0, 10000, 10000, 0, 10000)
    h_nsigmap = TH2F("nsigmap", "", 136, 264, 400, 192, 0, 192)
    
    collistw = {}
    collistwo = {}
    noiselist = []
    ReadJsonfile(fileNoise, noiselist)
    ReadRootfile(ws, collistw)

    EnablePixel(fileEn, noiselist, collistw, collistwo, h_rrandom, h_nw, h_nsig, h_nsigfit, h_nsigfitzoom, h_wsig, h_nsigmap, trigger, triggerw)
    FitPoisson(h_nsigfit, 0, 10, 1)
    FitPoisson(h_nsigfitzoom, 0, 10, 1)

    print("output")
    output.cd()
    h_rrandom.Write()
    h_nw.Write()
    h_nsig.Write()
    h_nsigfit.Write()
    h_nsigfitzoom.Write()
    h_wsig.Write()
    h_nsigmap.Write()
    output.Close()

    output1 = ROOT.TFile("ExtCompAna1.root", 'RECREATE')
    output1.cd()
    h_nw.Write()
    output1.Close()

#    output2 = ROOT.TFile("SelfCompAna2.root", 'RECREATE')
#    output2.cd()
#    h_nsig1.Write()
#    h_nsig.Write()
#    output2.Close()
#
    print("output OK ")
        
if __name__=='__main__':
    main()
