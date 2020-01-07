#!/usr/bin/env python

from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True

from ROOT import TH1F, TH2F, gStyle, TCanvas, gROOT, TLegend
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import numpy as np
import sys
import argparse

def HistoStyle(h, can, xname, yname):
    h.SetStats(0)
    h.SetFillStyle(3004)
    h.SetXTitle(xname)
    h.SetYTitle(yname)
    h.SetTitle("")
    h.SetLabelSize(0.045, "XY")
    h.SetTitleSize(0.050, "XY")
    h.SetLineWidth(2)

def LegendStyle(l):
    l.SetTextSize(0.045)
    l.SetTextFont(42)
    l.SetFillStyle(0)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    

def SaveCanvas(filename, objname, xname, yname, savename):
    f = open(filename, 'r')
    inpTFile = ROOT.TFile(filename, 'READ')

    can = ROOT.TCanvas()
    h = inpTFile.Get(objname)
    HistoStyle(h, can, xname, yname) 
    can.SetFrameLineWidth(2)
    can.SetTicks(1,1)

    if h == None:
        print('TObject not exist !!!!!')
    elif type(h)==TH1F:
        h.Draw()
    elif type(h)==TH2F:
        print(type(h))
        h.Draw("colz")
    can.SaveAs(savename+'.png')

def SaveCanvasDoub(filename, objname, xname, yname, savename, add, legend1, legend2, color):
    f1 = open(filename, 'r')
    inpTFile1 = ROOT.TFile(filename, 'READ')
    f2 = open(add, 'r')
    inpTFile2 = ROOT.TFile(add, 'READ')
    can = ROOT.TCanvas()
    h1 = inpTFile1.Get(objname)
    HistoStyle(h1, can, xname, yname)
    h2 = inpTFile2.Get(objname)
    HistoStyle(h2, can, xname, yname)

    can.SetFrameLineWidth(2)
    can.SetTicks(1,1)

    if h1 == None:
        print('TObject not exist !!!!!')
    elif type(h1)==TH1F and type(h2)==TH1F:
        if (color=="0"):
            h1.SetLineColor(kRed)
            h1.Draw()

            h2.SetLineColor(kBlue)
            h2.Draw("same")
        if (color=="1"):
            HistoStyle(h1, can, xname, yname)
            h1.SetLineColor(kBlue)
            h1.Draw("")
            HistoStyle(h2, can, xname, yname)
            h2.SetLineColor(kRed)
            h2.Draw("same")

    lg = TLegend(0.65, 0.75, 0.85, 0.85)
    LegendStyle(lg)
    lg.AddEntry(h1, legend1, "l")
    lg.AddEntry(h2, legend2, "l")
    lg.Draw()
    can.SaveAs(savename+'.png')


def main():
    parser = argparse.ArgumentParser(
        prog='Save Plots',
        usage='Save Canvas',
        description='description',
        epilog='end',
        add_help=True,
    )
    parser.add_argument('file', help='rootfile name to read', nargs=1)
    parser.add_argument('obj', help='object name in rootfile', nargs=1)
    parser.add_argument('xname', help='name of XAxis', nargs=1)
    parser.add_argument('yname', help='name of YAxis', nargs=1)
    parser.add_argument('save', help='name of savefile', nargs=1)
    parser.add_argument('-a', '--add', help='add file to draw same', nargs=1)
    parser.add_argument('-f', '--legend1', help='first legend', nargs=1)
    parser.add_argument('-s', '--legend2', help='second legend', nargs=1)
    parser.add_argument('-c', '--color', help='color type', nargs=1)
    parser.add_argument('-l', '--log', help='set logy style', nargs=1)

    args = parser.parse_args()
    print('start')
    #print(args.obj[0])

    gStyle.SetPalette(1)
    gStyle.SetLineWidth(2)
    gStyle.SetGridWidth(2);
    gStyle.SetHistLineWidth(2);

    gStyle.SetTitleSize(10);
    gStyle.SetStatFont(45);
    gStyle.SetLabelFont(42, "XYZ");
    gStyle.SetTitleFont(42, "XYZ");
    gStyle.SetTextFont(42);
    gStyle.SetLegendFont(42);

    if args.log:
        gStyle.SetOptLogy(1)

    if args.add:
        if args.legend1 and args.legend2:
            if args.color == None:
                SaveCanvasDoub(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0], args.add[0], args.legend1[0], args.legend2[0], 0)
            SaveCanvasDoub(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0], args.add[0], args.legend1[0], args.legend2[0], args.color[0])
        else:
            print("No Legend !!!")
    else:
        SaveCanvas(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0])

if __name__=='__main__':
    main()

