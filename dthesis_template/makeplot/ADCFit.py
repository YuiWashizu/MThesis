from ROOT import TH1F, gStyle, TCanvas, TLegend, TFile, TF1
from ROOT import kWhite, kBlack, kGray, kRed, kGreen, kBlue, kYellow, kMagenta, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kPink
import ROOT
import json
import numpy as np
import sys
from array import array

def FillHisto(fname, h):
    file = ROOT.TFile(fname, 'READ')
    print("import File Name : {}".format(fname))
    tree = file.Get('t')
    nevents = tree.GetEntries()
#    print("Create {} !".format(foutname))

    for ievent in range(nevents):
        tree.GetEntry(ievent)
        h.Fill(tree.adc0)
    
def Fit(h, nphotons, adcmin, adcmax):
    func0 = TF1('func0', '[0]*TMath::Gaus(x,[1],[2])', adcmin, 5050)
    func0.SetParameter(1, 5000)
    func0.SetParameter(2, 50)
    h.Fit("func0", "", "", adcmin, 5050)
    slope0 = func0.GetParameter(0)
    mean0 = func0.GetParameter(1)
    sigma0 = func0.GetParameter(2)

    print("mean0 : {}".format(mean0))
    print("sigma0 : {}".format(sigma0))

    func1 = TF1('func1', '[0]*TMath::Gaus(x,[1],[2])', 5000, 5200)
    func1.SetParameter(1, 5100)
    func1.SetParameter(2, 100)
    h.Fit("func1", "", "", 5000, 5200)
    sigma1 = func1.GetParameter(2)
    print("sigma1 : {}".format(sigma1))

    mean = []
    sigma = []
    slope = []
    d = 250
    for iphoton in range(nphotons):
        imean = mean0 + iphoton*d
        isigma = np.sqrt(iphoton)*sigma1
        mean.append(imean)
        sigma.append(isigma)


    func0 = TF1('func0', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func0.FixParameter(1, mean0)
    func0.FixParameter(2, sigma0)
    func1 = TF1('func1', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func1.FixParameter(1, mean[1])
    func1.FixParameter(2, sigma[1]) 
    func2 = TF1('func2', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func2.FixParameter(1, mean[2])
    func2.FixParameter(2, sigma[2])
    func3 = TF1('func3', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func3.FixParameter(1, mean[3])
    func3.FixParameter(2, sigma[3])
    func4 = TF1('func4', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func4.FixParameter(1, mean[4])
    func4.FixParameter(2, sigma[4])
    func5 = TF1('func5', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func5.FixParameter(1, mean[5])
    func5.FixParameter(2, sigma[5])
    func6 = TF1('func6', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func6.FixParameter(1, mean[6])
    func6.FixParameter(2, sigma[6])
    func7 = TF1('func7', '[0]*TMath::Gaus(x,[1],[2])', adcmin, adcmax)
    func7.FixParameter(1, mean[7])
    func7.FixParameter(2, sigma[7])
    functotal = TF1('functotal', 'func0+func1+func2+func3+func4+func5+func6+func7', adcmin, adcmax)
    h.Fit(func0, "R")
    h.Fit(func1, "R+")
    h.Fit(func2, "R+")
    h.Fit(func3, "R+")
    h.Fit(func4, "R+")
    h.Fit(func5, "R+")
    h.Fit(func6, "R+")
    h.Fit(func7, "R+")

    par0 = func0.GetParameters()
    par1 = func1.GetParameters()
    par2 = func2.GetParameters()
    par3 = func3.GetParameters()
    par4 = func4.GetParameters()
    par5 = func5.GetParameters()
    par6 = func6.GetParameters()
    par7 = func7.GetParameters()
    par = array( 'd', 24*[0.] )
    par[0], par[1], par[2] = par0[0], par0[1], par0[2]
    par[3], par[4], par[5] = par1[0], par1[1], par1[2]
    par[6], par[7], par[8] = par2[0], par2[1], par2[2]
    par[9], par[10], par[11] = par3[0], par3[1], par3[2]
    par[12], par[13], par[14] = par4[0], par4[1], par4[2]
    par[15], par[16], par[17] = par5[0], par5[1], par5[2]
    par[18], par[19], par[20] = par6[0], par6[1], par6[2]
    par[21], par[22], par[23] = par7[0], par7[1], par7[2]


    functotal.SetParameters(par)
    functotal.SetLineColor(kBlue+1)
    h.Fit(functotal, "R+")

def main():
    args = sys.argv
    fname = args[1]
    foutname = fname.strip('.root') + '_Fit.root'
    fout = ROOT.TFile(foutname, 'RECREATE')
    
    adc = TH1F("", "", 900, 3000, 12000)

    FillHisto(fname, adc)    
    Fit(adc, 8, 4800, 9000)

    fout.cd()
    adc.Write()
    fout.Close()
    

if __name__=='__main__':
    main()

