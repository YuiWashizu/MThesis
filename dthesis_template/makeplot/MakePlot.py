#!/usr/bin/env python

from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True

from ROOT import TH1F, TH2F, gStyle, TCanvas, gROOT
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
    h.SetXTitle(xname)
    h.SetYTitle(yname)
    if h == None:
        print('TObject not exist !!!!!')
    elif type(h)==TH1F:
        h.Draw()
    elif type(h)==TH2F:
        print(type(h))
        h.Draw("colz")
    can.SaveAs(savename+'.png')

def SaveCanvasDoub(filename, objname, xname, yname, savename, add):
    f = open(filename, 'r')
    inpTFile = ROOT.TFile(filename, 'READ')

    can = ROOT.TCanvas()
    h1 = inpTFile.Get(objname)
    h2 = inpTFile.Get(add)
    if h == None:
        print('TObject not exist !!!!!')
    elif type(h1)==TH1F and type(h2)==TH1F:
        h1.Draw()
        h2.Draw("same")
    h.SetStats(0)
    h.SetXTitle(xname)
    h.SetYTitle(yname)
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
        SaveCanvas(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0], args.add[0])
    else:
        SaveCanvas(args.file[0], args.obj[0], args.xname[0], args.yname[0], args.save[0])

if __name__=='__main__':
    main()

