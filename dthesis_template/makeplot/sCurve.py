#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TH2F, TGraph, gStyle, TCanvas
import ROOT
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
from array import array

def MakeData():
    args = sys.argv
    file = open(args[1], 'r')
    hist = []
    for line in file.readlines()[8:]:
        itemList = line.split(' ')
        numbers = []
        for item in itemList:
            if item == '\n':
                #print('enter end')
                break
                #print(int(item))
            numbers.append(int(item))
        hist.append(numbers)
    return hist

def MakeSCurve(hist):
    args = sys.argv
    #print(len(hist))
    #print(len(hist[1]))
    output = ROOT.TFile(args[1]+'.root', 'RECREATE')
    h2D = TH2F("sCurve", "", len(hist[1])-1, 0, (len(hist[1])-1)*5, len(hist)-1, 0, len(hist)-1)

    vcalList = []
    sumList = []
    c = TCanvas()
    tg = TGraph()

    for vcal in range(len(hist[1])):
        vcalsum = 0
        vcalList.append(int(vcal))
        for occ in range(len(hist)):
            h2D.SetBinContent(vcal, occ, hist[occ][vcal])
            #print(hist[occ][vcal])
            vcalsum = vcalsum + hist[occ][vcal]
            #print("SUM : {}".format(vcalsum))
        print(vcal)
        print(vcalsum)
        tg.SetPoint(tg.GetN(), vcal, vcalsum)

    tg.SetMarkerStyle(20)
    tg.SetMarkerSize(1.1)
    tg.Draw("AP")
    c.SaveAs("test.png")
        #sumList.append(float(vcalsum/len(hist)))
#    print(vcalList)
#    print(sumList)
#    print(len(hist[1]))
#   
#    plt.plot(vcalList, sumList)
#    plt.show()
    output.Add(tg)

    output.Write()


def main():
    MakeSCurve(MakeData())
    
        
if __name__=='__main__':
    main()
