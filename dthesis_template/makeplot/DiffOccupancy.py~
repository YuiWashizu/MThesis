from ROOT import TH2F, gStyle, TCanvas
import ROOT
import json
import numpy as np



def main():
    args = sys.argv
    inp = ROOT.TFile(args[1], 'READ')
    print("import File Name: {}\t".format(args[1]))
    inpt = inp.Get('HitTree')
    print("HitTree exist !!\t")
    outname = args[1].strip('.root') + 'output'
    output = ROOT.TFile(outname+'.root','RECREATE')
    
    h2D = TH2F("h2D", "", 136, 264, 399, 192, 1, 192)

    nevent = inpt.GetEntries()
    for ievent in range(nevent):
        inpt.GetEntry(ievent)
        if inpt.nhits != 0:
            for ihit in range(inpt.nhits):
                h2D.Fill(inpt.hit_col[ihit], inpt.hit_row[ihit])
    output.Write()
    print("Create {} ! \t".format(outname+'.root'))
    can = ROOT.TCanvas()
    h2D.Draw("colz")
    
    gStyle.SetPalette(1)
    h2D.SetXTitle("col")
    h2D.SetYTitle("row")
    h2D.SetStats(0)
    can.SaveAs(outname+'.png')

if __name__=='__main__':
    main()


