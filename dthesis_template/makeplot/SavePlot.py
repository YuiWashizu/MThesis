from ROOT import TH1F, TH2F, gStyle, TCanvas, gROOT
import ROOT
import json
import numpy as np
import sys

def main():

    args = sys.argv
    if len(args) < 7:
        print("./SavePlot.py readfile treename dimension xname yname savename")

    readfile = args[1]
    histname = args[2]
    dimension = args[3]
    xname = args[4]
    yname = args[5]
    savename = args[6]
    
    f = open(args[1], 'r')
    inpTFile = ROOT.TFile(readfile, 'READ')
    gStyle.SetPalette(1)
    gStyle.SetLineWidth(2)
    gStyle.SetGridWidth(2);
    gStyle.SetHistLineWidth(2);

    gStyle.SetTitleSize(10);
    gStyle.SetStatFont(42);
    gStyle.SetLabelFont(42, "XYZ");
    gStyle.SetTitleFont(42, "XYZ");
    gStyle.SetTextFont(42);
    gStyle.SetLegendFont(42);


    can = ROOT.TCanvas()

    #    if dimension == 1:
    #        h = inpTFile.Get(histname)
    #        h.SetStats(0)
    #           h.SetXTitle(xname)
    #            h.SetYTitle(yname)
    #            h.Draw()
    #    if args[3] == 2:
    h = inpTFile.Get(histname)
    print(type(h))
    h.SetStats(0)
    h.SetXTitle(xname)
    h.SetYTitle(yname)
    h.Draw("colz")

    can.SaveAs(savename)
    

if __name__=='__main__':
    main()

