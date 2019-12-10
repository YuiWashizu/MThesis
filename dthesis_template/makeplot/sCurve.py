#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TF1, TH1F, TH2F, TGraphErrors, gStyle, TCanvas
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
from array import array

def setHistoStyle(h, ms):
    size = 0.040

def MakeData(filename):
    file = open(filename, 'r')
    hist = []
    for line in file.readlines()[8:]:
        itemList = line.split(' ')
        numbers = []
#        print(itemList)
        for item in itemList:
            if item == '\n':
                #print('enter end')
                break
                #print(int(item))
            numbers.append(int(item))
        hist.append(numbers)
    return hist

def MakeSCurve(hist, h1d, h2d, scurveList):
    c = TCanvas()

    for vcal in range(len(hist[1])):
        occsum = 0
        evesum = 0
        occList = []
        for occ in range(len(hist)):
            for i in range(hist[occ][vcal]):
                occList.append(occ)
        scurveList.append(occList)
    print(scurveList[1])

def MakePlot(tge, scurveList):
    num = 0
    for i in scurveList:
        num = num + 5
        data = np.array(i)
        mean = np.mean(data)
        sig = np.std(data)
        n = tge.GetN()
        tge.SetPoint(n, num, mean)
        tge.SetPointError(n, 0, sig)

def fitGaus(fitgaus, h1d, p0, p1, p2, max, min):
    fitgaus.SetParameter(0, p0)
    fitgaus.SetParameter(1, p1)
    fitgaus.SetParameter(2, p2)
    h1d.Fit("fitgaus", "", "", max, min)
    
def main():
    args = sys.argv
    filename = args[1]
    output = ROOT.TFile(args[1]+'.root', 'RECREATE')

    #define histogram
    h2D = TH2F("sCurve", "", 61, -2.5, 302.5, 49, 0.5, 49.5)
    h1D = TH1F("VcalConst", "", 49, 0.5, 49.5)

    #define TGraphErrors
    tge = TGraphErrors()
    tge.SetMarkerColor(kBlack)
    tge.SetMarkerStyle(22)

    #define fit function
    fitgaus = TF1("fitgaus","[2]*(1+(TMath::Erf((x-[0])/sqrt(2*[1]))))",0,300)
    fitgaus.SetLineColor(kBlue+1)

    hist = MakeData(filename)
    scurveList = []

    c = TCanvas()

    MakeSCurve(hist, h1D, h2D, scurveList)
    MakePlot(tge, scurveList)
    
    setHistoStyle(fitgaus, 20) 
    gStyle.SetLineWidth(2)
    gStyle.SetTitleSize(0.040, "X" )
    gStyle.SetTitleSize( 0.040, "Y" )
    gStyle.SetLabelSize( 0.040, "X" )
    gStyle.SetLabelSize( 0.040, "Y" )
    c.DrawFrame(0, 0, 300, 50)
    tge.SetMarkerSize(1.1)
    tge.SetMaximum(0)
    tge.SetMinimum(50)    
    tge.Draw("P")
    fitGaus(fitgaus, tge, 240, 25, 25, 0, 300)
    c.SaveAs("../figure/sCurve.png")
   
    
        
if __name__=='__main__':
    main()
