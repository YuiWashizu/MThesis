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
 
def EnablePixel(filename, noiselist, collistw, collistwo, noisefreq, hitsperpixwo, hitsperpixwocut, hitsperpixwobfaf, hitsperpixw, hitsperpixwcut, hitsperpixwbfaf, trigger, triggerw, triggerwo):
    f = open(filename, 'r')
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

    for col in range(264, 400):
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in range(0, 192):
            if colnum["Enable"][int(row)] == 1:
                nrandom = noiselist[row][col] # N_random
                rrandom = float(nrandom)/float(trigger) # R_random
                nw = len(collistw[col][row]) # N_w
                nwo = len(collistwo[col][row]) # N_wo
                nw = len(collistw[col][row]) # N_w
                rwo = float(nwo) / float(triggerwo) # R_wo
                rw = float(nw) / float(triggerw) # R_w
                nsensor = int(nhitswo) - int(float(rrandom)*float(triggerwo)) # N_sensor
                rsensor = float(nsensor) / float(triggerwo) # R_sensor
                nsig1 = int(nhitsw) - int(float(rrandom)*float(triggerw))
                nsig = nsig1 - int(float(rsensor)*float(triggerw)) #n_signal

                if nsensor < 0:
                    nsensor = 0
                if nsig1 < 0:
                    nsig1 = 0
                if nsig < 0:
                    nsig = 0

                noisefreq.Fill(noise)
                hitsperpixwo.Fill(nhitswo)
                hitsperpixwocut.Fill(nhitswocut)
                hitsperpixwobfaf.Fill(nhitswo, nhitswocut)

                hitsperpixw.Fill(nhitsw)
                hitsperpixwcut.Fill(nhitswcut)
                hitsperpixwbfaf.Fill(nhitsw, nhitswcut)
                

#                if nhitswo == 0:a
#                     switch = 0
#                    #with source                        
#                    noisefreq3.Fill(noise)
#                    hitsperpix3w.Fill(nhitsw)
#                    hitsperpix3cut.Fill(nhitwcut)
#                    hitsperpix3bfaf.Fill(nhitsw, nhitwcut)
#
#                    if nhitsw != 0:
#                        for itot in collistw[col][row]:
#                            if itot > 0:
#                                switch = 1
#                        if switch == 1:
#                            nhits3 = nhits3 + nhitsw
#                            pixel3 += 1
#                        else:
#                            nhits3dbg = nhits3dbg + nhitsw
#                            pixel3dbg += 1
                    #patern 4
#                else:
#                    print("noise     : {}".format(noise))
#                    print("nhitsw    : {}".format(nhitsw))
#                    print("nhitswcut : {}".format(nhitwcut))
#                    noisefreq4.Fill(noise)
#                    hitsperpix4w.Fill(nhitsw)
#                    hitsperpix4cut.Fill(nhitwcut)
#                    hitsperpix4bfaf.Fill(nhitsw, nhitwcut)
#                    hitsperpix4bfafzoom.Fill(nhitsw, nhitwcut)
#
#                    hitsperpix.Fill(nhitsw)
#                    hitsperpixcut.Fill(nhitwcut)
#                    hitsperpixcutfit.Fill(nhitwcut)
#                    hitsperpixbfaf.Fill(nhitsw, nhitwcut)
#                    n = 0.
#                    nbg = 0.
#                    nsigratio = 0.
#                    hitsperpix4w.Fill(nhitsw)
#                    hitsperpix4wo.Fill(nhitswo)
##                       for itot in collistw[col][row]:
#                           if itot > 5:
#                               n += 1
#                       for itot in collistwo[col][row]:
#                           if itot > 5:
#                               nbg += 1
#                       nsig = n/trigw - nbg/trigwo
#                       sigma = np.sqrt(nbg/trigwo)
#                       if nsig/sigma > 5.:
#                           nsigratio = nsig/(n/trigw)
#                           nhits4 = nhits4 + n*nsigratio
#                           pixel4 += 1
#                           print("n    : {}".format(n))
#                           print("nbg  : {}".format(nbg))
#                           print("nsig : {}".format(nsig))
#                           print("nhits: {}".format(n*nsigratio))
#                       else:
#                           pixel4dbg += 1
#
#    print("nhits3    : {}".format(nhits3))
#    print("nhits4    : {}".format(nhits4))
#    print("pixel3    : {}".format(pixel3))
#    print("pixel3dbg : {}".format(pixel3dbg)) 
#    print("pixel4    : {}".format(pixel4))
#    print("pixel4dbg : {}".format(pixel4dbg))

def FitPoisson(hist, hitmin, hitmax, mean):
    poisson = TF1('poisson', '[0]*TMath::Poisson(x,[1])', hitmin, hitmax)
    poisson.SetParameter(0, 35000)
    poisson.SetParameter(1, mean)
    hist.Fit("poisson", "", "", hitmin, hitmax)
    slope0 = poisson.GetParameter(0)
    mean0 = poisson.GetParameter(1)

    print("mean0 : {}".format(mean0))


def main():
    args = sys.argv
    ws = args[1]
    wos = args[2]
    fileNoise = "./data/015894_std_noisescan_KEK53-4/JohnDoe_Occupancy.dat"
    fileEn = "./data/015902_std_exttrigger_KEK53-4/rd53a_test.json.before"
    outputw = ROOT.TFile(ws + "_Ana.root", 'RECREATE')
    outputwo = ROOT.TFile(wos + "_Ana.root", 'RECREATE')
    trigger = 200000 * 300
    triggerw = 4056311
    triggerwo = 4193685

    h_rrandom = TH1F("rrandom", "", trigger, 0, 1)
    h_nwo = TH1F("nhits", "", 10000, 0, 10000)
    h_nw = TH1F("", "", 10000, 0, 10000)
    h_nsensor = TH2F("nhits", "", 10000, 0, 10000, 10000, 0, 10000)
    h_nsig1 = TH1F("nsig1", "", 10000, 0, 10000)
    h_nsig = TH1F("nsig", "", 10000, 0, 10000)
    h_wosensor = TH2F("NwoVSNsensor", "", 10000, 0, 10000, 10000, 0, 10000)
    h_wsig1 = TH2F("NwVSNsig1", "", 100000, 0, 100000, 10000, 0, 10000)
    h_wsig = TH2F("NwVSNsig", "", 100000, 0, 100000, 10000, 0, 10000)
    
    collistw = {}
    collistwo = {}
    noiselist = []
    ReadJsonfile(fileNoise, noiselist)
    ReadRootfile(ws, collistw)
    ReadRootfile(wos, collistwo)

    EnablePixel(fileEn, noiselist, collistw, collistwo, noisefreq, hitsperpixwo, hitsperpixwocut, hitsperpixwobfaf, hitsperpixw, hitsperpixwcut, hitsperpixwbfaf, trigger, triggerw, triggerwo)
#    FitPoisson(hitsperpixcut, 0, 10000, 20)

    print("output")
    outputw.cd()
#    hitsperpixw.Write()
#    hitsperpixwcut.Write()
    hitsperpixwbfaf.Write()
    outputw.Close()

    outputwo.cd()
    noisefreq.Write()
#    hitsperpixwo.Write()
#    hitsperpixwocut.Write()
#    hitsperpixwobfaf.Write()
    outputwo.Close()
    print("output OK ")
        
if __name__=='__main__':
    main()
