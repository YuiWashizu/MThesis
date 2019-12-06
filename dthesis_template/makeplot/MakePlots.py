from ROOT import TH2F, gStyle, TCanvas
import ROOT
import json
import numpy as np
import sys

def readjson():
    args = sys.argv
    jsonfile = args[1] + '/rd53a_test.json.before'
    f = open(jsonfile, 'r')
    json_data = json.load(f)

    h2D = TH2F("h2D", "", 136, 264, 399, 191, 1, 191)
    col_list = np.linspace(264., 399., 136.)
    row_list = np.linspace(1., 191., 191.)
    for col in col_list:
        colnum = json_data["RD53A"]["PixelConfig"][int(col)]
        for row in row_list:
            if colnum["Enable"][int(row)] == 1:
                h2D.Fill(col, row)    
    return h2D

def diffhitmap():
    args = sys.argv
    rootfile = args[1] + '/JohnDoe_0_data.root'
    inp = ROOT.TFile(rootfile, 'READ')
    inpt = inp.Get('HitTree')

    h2D = TH2F("h2D", "", 136, 264, 399, 191, 1, 191)
    nevent = inpt.GetEntries()
    for ievent in range(nevent):
        inpt.GetEntry(ievent)
        if inpt.nhits != 0:
            for ihit in range(inpt.nhits):
                h2D.Fill(inpt.hit_col[ihit], inpt.hit_row[ihit])
    return h2D


def 2dPlot(h2D, savename):
    can = ROOT.TCanvas()
    h2D.Draw("colz")    
    h2D.SetXTitle("col")
    h2D.SetYTitle("row")
    h2D.SetStats(0)
    can.SaveAs(savename)

def main():
    args = sys.argv
    OutName = args[1] + '/MakeSomePlots'
    OutTFile = ROOT.TFile(OutName+'.root', 'RECREATE')
    
    DiffEnablePix = readjson()
    DiffOccupancy = diffhitmap()

    OutTFile.Write()

    if args[2] == 1:
        2dPlot(DiffEnablePix, OutName+'_DiffEnablePix.png')
        2dPlot(DiffEnablePix, OutName+'_DiffOccupancy.png')
        

if __name__=='__main__':
    main()


