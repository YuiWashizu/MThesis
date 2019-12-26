#!/usr/bin/env python

from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True

from ROOT import TH1F, TH2F, gStyle, TCanvas, gROOT
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import numpy as np
import sys
import argparse


def SaveCanvas(filename, objname, xname, yname, savename):
    f = open(filename, 'r')
    inpTFile = ROOT.TFile(filename, 'READ')

    can = ROOT.TCanvas()
    h = inpTFile.Get(objname)
    h.SetStats(0)
    h.SetFillStyle(3004)
    h.SetXTitle(xname)
    h.SetYTitle(yname)
    if h == None:
        print('TObject not exist !!!!!')
    elif type(h)==TH1F:
        can.SetFrameLineWidth(2)
        h1.SetLabelSize(0.035, "XY")
        h1.SetTitleSize(0.040, "XY")
        h1.SetLineWidth(2)
        h.Draw()
    elif type(h)==TH2F:
        print(type(h))
        h.Draw("colz")
    can.SaveAs(savename+'.png')

def SaveCanvasDoub(filename, objname, xname, yname, savename, add):
    f1 = open(filename, 'r')
    inpTFile1 = ROOT.TFile(filename, 'READ')
    f2 = open(add, 'r')
    inpTFile2 = ROOT.TFile(add, 'READ')

    can = ROOT.TCanvas()
    h1 = inpTFile1.Get(objname)
    h2 = inpTFile2.Get(objname)
    if h1 == None:
        print('TObject not exist !!!!!')
    elif type(h1)==TH1F and type(h2)==TH1F:
        h1.SetLineColor(kRed)
        h1.Draw()
        h2.SetLineColor(kBlue)
        h2.Draw("same")
    h1.SetStats(0)
    h1.SetXTitle(xname)
    h1.SetYTitle(yname)

    can.SetFrameLineWidth(2)
    h1.SetLabelSize(0.035, "XY")
    h1.SetTitleSize(0.040, "XY")
    h1.SetLineWidth(2)
    h2.SetLabelSize(0.035, "XY")
    h2.SetTitleSize(0.040, "XY")
    h2.SetLineWidth(2)
    can.SaveAs(savename+'.png')


def main():
    parser = argparse.ArgumentParser(
        prog='Save Plots',
        usage='Save Canvas',
        description='description',
        epilog='end',
        add_help=True,
    )
    parser.add_argument('-f', '--file', help='rootfile name to read', nargs=1)
    parser.add_argument('-o', '--obj', help='object name in rootfile', nargs=1)
    parser.add_argument('-x', '--xname', help='name of XAxis', nargs=1)
    parser.add_argument('-y', '--yname', help='name of YAxis', nargs=1)
    parser.add_argument('-s', '--save',  help='name of savefile', nargs=1)
    parser.add_argument('-a', '--add', help='add file to draw same', nargs=1)

    args = parser.parse_args()
    print('start')
    print(args.obj[0])

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


    if args.add:
        SaveCanvasDoub(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0], args.add[0])
    else:
        SaveCanvas(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0])

if __name__=='__main__':
    main()

