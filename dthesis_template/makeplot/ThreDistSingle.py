#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TH1F, gStyle, TCanvas, TLegend
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import numpy as np
import sys


def MakeData(filename):
    file = open(filename, 'r')    
    lineList = []
    for line in file.readlines()[5:]:
        linefix = line.replace('\n', '')
        itemList = linefix.split(' ')
        numbers = []
        for item in itemList:                    
            if item == '':
                print('NULL')
                break
            numbers.append(int(item))
        lineList.append(numbers)
    return lineList


def FillHisto(filename, h1D):
    lineList = MakeData(filename)
    bin = lineList[0][0]
    min = lineList[0][1]
    max = lineList[0][2]
    minbin = h1D.FindBin(min)
    maxbin = h1D.FindBin(max)
    print('bin : {0}, min : {1}, max : {2}'.format(bin, min, max))
    print('minbin : {0}, maxbin : {1}'.format(minbin, maxbin))
    thre = minbin - 1
    for eve in lineList[2]:
        thre = thre + 1 
        h1D.SetBinContent(thre, eve)
        #print('(thre, eve) = ({0}, {1})'.format(thre, eve))

def SetLegendStyle(l):
    l.SetTextSize(0.04)
    l.SetTextFont(42)
    l.SetFillStyle(0)
    l.SetFillColor(0)
    l.SetBorderSize(0)

def setHistoStyle(h, lc, ms):
    size = 0.040
    h.SetStats(0)
    h.SetLineColor(lc)
    h.SetLineWidth(2)
    h.SetTitleOffset( 1.3, "X" )
    h.SetTitleOffset( 1.3, "Y" )
    h.SetTitleSize( size, "X" )
    h.SetTitleSize( size, "Y" )
    h.SetLabelSize( size, "X" )
    h.SetLabelSize( size, "Y" )

def main():
    args = sys.argv
    filename1 = args[1]
    output1 = ROOT.TFile(args[1]+'.root', 'RECREATE')
z
    Thr = TH1F("ThreDist", "", 409, -5, 4085)


    #data fill
    FillHisto(filename1, Thr)    
    Thr.Draw("")
    output1.Write()
        
if __name__=='__main__':
    main()
