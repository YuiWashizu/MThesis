/*
  LatencyAnalysis
*/
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TH2.h"
#include "TF2.h"
#include "TTree.h"
#include "TStyle.h"
#include <stdio.h>
#include <math.h>
#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <string>
#include <sstream>


void CutZeroEvents(std::string fname) {
  std::string impfname = fname + "/JohnDoe_0_data.root";
  TFile *f = TFile::Open(impfname.c_str(), "READ");
  TTree *t = dynamic_cast<TTree*>(f->Get("HitTree"));
  
  std::string outfname = fname + "/JohnDoe_0_data_output.root";
  TFile* fout = new TFile(outfname.c_str(), "RECREATE");
  // float sec = min*60;
  // plt.Style();
  
  int ievent;
  int nevents = t->GetEntries();
  int nhits;
  int l1id;
  int hit_col[10000];
  int hit_row[10000];
  int hit_tot[10000];
    
  t->SetBranchAddress("nhits", &nhits);
  t->SetBranchAddress("hit_l1id", &l1id);
  t->SetBranchAddress("hit_col", &hit_col);
  t->SetBranchAddress("hit_row", &hit_row);
  t->SetBranchAddress("hit_tot", &hit_tot);

  int ihit;
  TH1* nhits_dist = new TH1F("nhits", "nhits;nhits;events", 10, 0, 10);
  TH1* tot = new TH1F("tot", "ToT;ToT;events", 15, 0, 15);
  TH1* l1dist = new TH1F("l1dist", "L1Dist;L1id;events", 16, 0, 16);
  // TH1 *col_dist = new TH1F("col_dist", "HitDist;col;events", 136, 264, 400);
  // TH1 *row_dist = new TH1F("row_dist", "HitDist;row;events", 96, 0, 96);
  TH2 *hitmap = new TH2F("hitmap", "HitMap;col;row", 136, 264, 399, 192, 0, 191);
  TH2* HitperTrig = new TH2F("# hits per trig", "# hits per trig;col;row", 136, 264, 399, 192, 0, 192);

  int countNonZero = 0;
  double counthit;
  float trig = nevents/16;

  for (ievent=0; ievent<nevents; ievent++) { 
    t->GetEntry(ievent);
    if (nhits!=0) {
      nhits_dist->Fill(nhits);
      l1dist->Fill(l1id%16);
      for (ihit=0; ihit<nhits; ihit++) {
	// col_dist->Fill(hit_col[ihit], 1/sec);
	// row_dist->Fill(hit_row[ihit], 1/sec);
	hitmap->Fill(hit_col[ihit], hit_row[ihit]);
	HitperTrig->Fill(hit_col[ihit], hit_row[ihit], 1/trig);
	tot->Fill(hit_tot[ihit]);
      }
    }
  }    

  fout->Write();
}




