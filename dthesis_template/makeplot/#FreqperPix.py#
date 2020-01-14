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

def Make2DHisto(hist, h, time):
    for col in range(0, 136):
        for row in range(0, 191):
            hits = hist[row][col+264]
            if hits!=0:
                #print(h2D.GetBin(col, row))
                h.Fill(hist[row][col+264])
    
def main():
    args = sys.argv
    filename = args[1]
    time = args[2]
    output = ROOT.TFile(args[1]+'_freqZoom.root', 'RECREATE')
    hist = []
    #define histogram
    freq = TH1F("freq", "", 50, 0, 50)

    MakeData(hist, filename)

    Make2DHisto(hist, freq, time)
    gStyle.SetTitleSize(0.040, "X" )
    gStyle.SetTitleSize( 0.040, "Y" )
    gStyle.SetLabelSize( 0.040, "X" )
    gStyle.SetLabelSize( 0.040, "Y" )
    freq.Draw("")
    output.Write()
    
        
if __name__=='__main__':
    main()
