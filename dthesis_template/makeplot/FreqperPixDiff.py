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


def Make2DHistoDiff(histw, histwo, h1, h2, outputw, outputwo):
    for col in range(0, 136):
        for row in range(0, 191):
            hits = histw[row][col+264]
            if hits!=0:
                #print(h2D.GetBin(col, row))
                h2.Fill(histwo[row][col+264])
                h1.Fill(histw[row][col+264])


def main():
    args = sys.argv
    filenamew = args[1]
    filenamewo = args[2]
    outputw = ROOT.TFile(filenamew + '_freq.root', 'RECREATE')
    outputwo = ROOT.TFile(filenamewo + '_freq.root', 'RECREATE')
    histw = []
    histwo = []

    #define histogram
    freqw = TH1F("freq", "", 180000, 0, 180000)
    freqwo = TH1F("freq", "", 180000, 0, 180000)

    MakeData(histw, filenamew)
    MakeData(histwo, filenamewo)
#    print(histwo)
    print(type(freqwo))

    Make2DHistoDiff(histw, histwo, freqw, freqwo, outputw, outputwo)

    outputwo.cd()
    freqwo.Write()
    outputwo.Close()

    outputw.cd()
    freqw.Write()
    outputw.Close()

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
