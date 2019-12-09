#!/usr/bin/python
# -*- coding: utf-8 -*-

from ROOT import TH1F, gStyle, TCanvas
import ROOT
import json
import numpy as np
import sys


def MakeData():
    args = sys.argv
    file = open(args[1], 'r')
    for line in file.readlines()[7:]:
        itemList = line.split(' ')
        numbers = []
        for item in itemList:
            if item == '\n':
                print('enter end')
                break
                #print(int(item))
            numbers.append(int(item))
    return numbers

def MakeRootFile(numbers):
    args = sys.argv
    print(len(numbers))
    output = ROOT.TFile(args[1]+'.root', 'RECREATE')
    h1D = TH1F("ThreDist", "", len(numbers), 0, len(numbers)*10)
    for i in range(len(numbers)):
        h1D.SetBinContent(i, numbers[i])
    output.Write()

def main():
    MakeRootFile(MakeData())
    
        
if __name__=='__main__':
    main()
