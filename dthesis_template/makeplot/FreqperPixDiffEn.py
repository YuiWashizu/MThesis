#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TF1, TH1F, TH2F, TGraph, gStyle, TCanvas
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
from array import array

def setHistoStyle(h, ms):
    size = 0.040

def MakeData(hist, filename):
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
            numbers.append(int(item))
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
        #print(len(rowlist))
        if (ievent%192 == 191):
            collist[int(ievent/192)] = rowlist
#            print("ievent%400")
            rowlist = []
    print(collist[397][139])
    print(len(collist))
    print(len(collist[397]))
 
def EnablePixel(filename, histw, histwo, h1, h2, h3, collist, tot1, tot2, tot3, tot4):
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    nhits1 = 0
    nhits2 = 0
    nhits3 = 0
    nhits4 = 0

    f = open(filename, 'r')
    json_data = json.load(f)

#    print("histw    : {}".format(histw[138][396]))
#    print("histwo   : {}".format(histwo[138][396]))
#    print("collist  : {}".format(collist[397][139]))
#    print("collist  : {}".format(len(collist[397][139])))
#    print("histw    : {}".format(histw[192][400]))
#    print("collist  : {}".format(collist[400][192]))
#
    for col in range(0, 135):
        colnum = json_data["RD53A"]["PixelConfig"][int(col+264)]
        for row in range(0, 191):
            if colnum["Enable"][int(row)] == 1:
                h1.Fill(histw[row][col+264])
                h2.Fill(histwo[row][col+264])
                if histwo[row][col+264] == 0:
                    if histw[row][col+264] == 0:
                        p1 += 1
                        nhits1 = nhits1 + len(collist[col+265][row+1])
                        for itot in collist[col+265][row+1]:
                            tot1.Fill(itot)
                    else:
                        p3 += 1
                        nhits3 = nhits3 + len(collist[col+265][row+1])
                        for itot in collist[col+265][row+1]:
                            tot3.Fill(itot)
                else:
                    if histw[row][col+264] == 0:
                        p2 += 1
                        nhits2 = nhits2 + len(collist[col+265][row+1])
                        for itot in collist[col+265][row+1]:
                            tot2.Fill(itot)
                    else:
                        p4 += 1
                        nhits4 = nhits4 + len(collist[col+265][row+1])
                        for itot in collist[col+265][row+1]:
                            tot4.Fill(itot)
    print("zero zero   : {}".format(p1))
    print("zero !zero  : {}".format(p2))
    print("!zero zero  : {}".format(p3))
    print("!zero !zero : {}".format(p4))
    print("zero zero   : {}".format(nhits1))
    print("zero !zero  : {}".format(nhits2))
    print("!zero zero  : {}".format(nhits3))
    print("!zero !zero : {}".format(nhits4))


def main():
    args = sys.argv
    filenamew = args[1]
    filerootw = args[2]
    filenamewo = args[3]
    filerootwo = args[4]
    fileEn = "./data/015902_std_exttrigger_KEK53-4/rd53a_test.json.before"
    outname = args[5]
    outputw = ROOT.TFile(filenamew + '_freqw.root', 'RECREATE')
    outputwo = ROOT.TFile(filenamewo + '_freqwo.root', 'RECREATE')
    output = ROOT.TFile(outname, 'RECREATE')
    
    histw = []
    histwo = []
    collist = {}
    ReadRootfile(filerootw, collist)
    print(len(collist))
    MakeData(histw, filenamew)
    MakeData(histwo, filenamewo)
    print(len(histw))
    print(len(histwo))

    #define histogram
    freqw = TH1F("freq", "", 180000, 0, 180000)
    freqwo = TH1F("freq", "", 180000, 0, 180000)
    zero = TH1F("zero", "", 100, 0, 100)
    tot1 = TH1F("tot1", "", 16, 0, 16)
    tot2 = TH1F("tot2", "", 16, 0, 16)
    tot3 = TH1F("tot3", "", 16, 0, 16)
    tot4 = TH1F("tot4", "", 16, 0, 16)

    EnablePixel(fileEn, histw, histwo, freqw, freqwo, zero, collist, tot1, tot2, tot3, tot4)

    outputw.cd()
    freqw.Write()
    outputw.Close()

    outputwo.cd()
    freqwo.Write()
    outputwo.Close()

    output.cd()
    tot1.Write()
    tot2.Write()
    tot3.Write()
    tot4.Write()
    zero.Write()
    output.Close()

    gStyle.SetTitleSize(0.040, "X" )
    gStyle.SetTitleSize( 0.040, "Y" )
    gStyle.SetLabelSize( 0.040, "X" )
    gStyle.SetLabelSize( 0.040, "Y" )
#    freqwo.Draw("")
#    freqw.Draw("same")
#    output.Write()
#    
        
if __name__=='__main__':
    main()
