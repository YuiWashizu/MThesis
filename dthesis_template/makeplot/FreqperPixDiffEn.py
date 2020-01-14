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


def EnablePixel(filename, histw, histwo, h1, h2):
    f = open(filename, 'r')
    json_data = json.load(f)
#    pix_list = ["Col", "Enable", "Hitbus", "InjEn", "TDAC"]
    for col in range(0, 136):
        colnum = json_data["RD53A"]["PixelConfig"][int(col+264)]
        for row in range(0, 191):
#            print("before if")
            if colnum["Enable"][int(row)] == 1:
                h1.Fill(histw[row][col+264])
                h2.Fill(histwo[row][col+264])

def main():
    args = sys.argv
    filenamew = args[1]
    filenamewo = args[2]
    filenameen = args[3]
    outputw = ROOT.TFile(filenamew + '_freqEn.root', 'RECREATE')
    outputwo = ROOT.TFile(filenamewo + '_freqEn.root', 'RECREATE')
    histw = []
    histwo = []

    #define histogram
    freqw = TH1F("freq", "freqw", 180000, 0, 180000)
    freqwo = TH1F("freq", "freqwo", 180000, 0, 180000)

    MakeData(histw, filenamew)
    MakeData(histwo, filenamewo)
    EnablePixel(filenameen, histw, histwo, freqw, freqwo)
    print("freqw  : {}".format(type(freqw)))
    print("freqwo : {}".format(type(freqwo)))

    outputw.cd()
    freqw.Write()
    outputw.Close()

    print("freqw  : {}".format(type(freqw)))
    print("freqwo : {}".format(type(freqwo)))


    outputwo.cd()
    freqwo.Write()
    outputwo.Close()


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
