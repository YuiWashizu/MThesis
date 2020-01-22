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
            numbers.append(float(item))
        hist.append(numbers)

def perPix(noiselist, trigger, hist):
    for col in range(264, 400):
        for row in range(0, 192):
            noise = noiselist[row][col]/float(trigger)
            hist.Fill(noise)
    
def main():
    args = sys.argv
    filename = args[1]
    output = ROOT.TFile(args[1]+'.root', 'RECREATE')
    hist = []
    #define histogram
    trigger = 200000 * 300
    noisefreq= TH1F("noisefreq", "", trigger, 0, 1)

    MakeData(hist, filename)
    perPix(hist, trigger, noisefreq)

    output.Write()
    
        
if __name__=='__main__':
    main()
