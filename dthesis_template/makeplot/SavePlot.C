#include "TTree.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TLegend.h"
#include "TPaveStats.h"
#include <stdio.h>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>

void Frame(int linewd, int fontid) {
  gStyle->SetPalette(55);
  gStyle->SetLineWidth(linewd);
  gStyle->SetGridWidth(linewd);
  gStyle->SetHistLineWidth(linewd);

  gStyle->SetTitleSize(10);
  gStyle->SetStatFont(fontid);
  gStyle->SetLabelFont(fontid, "XYZ");
  gStyle->SetTitleFont(fontid, "XYZ");
  gStyle->SetTextFont(fontid);
  gStyle->SetLegendFont(fontid);
}


void SavePlot(std::string fname, std::string treename, std::string savename, int canx, int cany, std::string xname, std::string yname) {
  std::cout << "std::string fname, std::string treename, std::string savename, int canx, int cany, std::string xname, std::string yname" << std::endl;
  TFile *f = TFile::Open(fname.c_str(), "READ");
  TH1F *hist = (TH1F*)f->Get(treename.c_str());
  Frame(2, 42);
  gStyle->SetOptStat(0);

  TCanvas* c1 = new TCanvas("c1", "c1", canx, cany);
  hist->Draw();
  hist->SetXTitle(xname.c_str());
  hist->SetYTitle(yname.c_str());
  hist->SetLabelSize(0.05, "XY");
  hist->SetTitleSize(0.05, "XY");
  // c1->SetLogy();
  c1->SaveAs(savename.c_str());
}
