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

def Make2DHisto(hist, h2D, hits):
    for col in range(0, 136):
        for row in range(0, 191):
            #print(h2D.GetBin(col, row))
            h2D.SetBinContent(h2D.GetBin(col, row), hist[row][col+264])
            hits = hits + hist[row][col+264]
    print("hits : {}".format(hits))
    
def main():
    args = sys.argv
    filename = args[1]
    time = args[2]
    output = ROOT.TFile(args[1]+'_trigrate.root', 'RECREATE')
    hist = []
    hits = 0
    #define histogram
    h2D = TH2F("hitmap", "", 136, 264, 400, 191, 0, 191)

    MakeData(hist, filename)

    Make2DHisto(hist, h2D, hits)
    gStyle.SetTitleSize(0.040, "X" )
    gStyle.SetTitleSize( 0.040, "Y" )
    gStyle.SetLabelSize( 0.040, "X" )
    gStyle.SetLabelSize( 0.040, "Y" )
    h2D.Draw("")
    output.Write()
    print(hits)
    trigrate = hits/int(time)
    print("Trigger Rate : {}".format(trigrate))
    
        
if __name__=='__main__':
    main()
