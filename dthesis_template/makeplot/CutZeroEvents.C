/*
  LatencyAnalysis
*/
#undef fromHitTree_cxx

#include "fromHitTree.h"
#include "./scripts/AppGraph.h"

void CutZeroEvents(std::string fname, int min) {
  AppGraph plt;
  TTree* t = plt.ReadFile(fname, "HitTree");
  fname.erase(fname.end()-5, fname.end());
  TFile* fout = plt.OutputFile(fname);
  float sec = min*60;
  plt.Style();
  
  fromHitTree event(t);
  int ievent;
  long long int nevents = t->GetEntries();
  int ihit;
  TH1* nhits = new TH1F("nhits", "nhits;nhits;events", 10, 0, 10);
  TH1* tot = new TH1F("tot", "ToT;ToT;events", 15, 0, 15);
  TH1* l1dist = new TH1F("l1dist", "L1Dist;L1id;events", 16, 0, 16);
  TH1 *col_dist = new TH1F("col_dist", "HitDist;col;events", 136, 264, 400);
  TH1 *row_dist = new TH1F("row_dist", "HitDist;row;events", 96, 0, 96);
  TH2 *hitmap = new TH2F("hitmap", "HitMap;col;row", 136, 263.5, 399.5, 191, -0.5, 191.5);
  TH2* HitperTrig = new TH2F("# hits per trig", "# hits per trig;col;row", 136, 263.5, 399.5, 191, -0.5, 191.5);

  int countNonZero = 0;
  double counthit;
  float trig = nevents;

  for (ievent=0; ievent<nevents; ievent++) { 
    event.GetEntry(ievent);
    if (event.nhits!=0) {
      countNonZero++;
      nhits->Fill(event.nhits);
      l1dist->Fill(event.hit_l1id%16);
      counthit = counthit + event.nhits;
      for (ihit=0; ihit<event.nhits; ihit++) {
	col_dist->Fill(event.hit_col[ihit], 1/sec);
	row_dist->Fill(event.hit_row[ihit], 1/sec);
	hitmap->Fill(event.hit_col[ihit], event.hit_row[ihit]);
	HitperTrig->Fill(event.hit_col[ihit], event.hit_row[ihit], 1/trig);
	tot->Fill(event.hit_tot[ihit]);
      }
    }
  }    

  // for (int col=1; col<137; col++) {
  //   for (int row=1; row<193; row++) {
  //     int hits1 = hitmap->GetBinContent(col, row);
  //     // int hits2 = hitmap_c->GetBinContent(col, row);
  //     // std::cout << "hits[" << col << "][" << row << "] = " << hits << std::endl;
  //     if (hits1!=0) {
  // 	EventsperPix1->Fill(hits1);
  //     }
  //     if (hits2!=0) {
  // 	EventsperPix2->Fill(hits2);
  //     }
  //   }
  // }

  std::cout << "AllEvents          = " << nevents << std::endl;
  std::cout << "countNonZeroEvents = " << countNonZero << std::endl;
  std::cout << "num of hits        = " << counthit << std::endl;
  std::cout << "# hits per sec     = " << counthit/(min*60) << std::endl;
  fout->Write();

  std::string ofs_name = fname + ".txt";
  ofstream ofs(ofs_name.c_str());  
  ofs << "AllEvents          = " << nevents << "\n"
      << "countNonZeroEvents = " << countNonZero << "\n"
      << "num of hits        = " << counthit << "\n"
      << "# hits per sec     = " << counthit/(min*60) << std::endl;
  
  
  TCanvas* c1 = plt.Hist1d(nhits, 700, 500);
  // plt.AddStats(c1, nhits, 1);
  plt.SaveAs(c1, fname, "_nhits.png");
  TCanvas* c2 = plt.Hist2dLogz(hitmap, 700, 500);
  plt.SaveAs(c2, fname, "_hitmap.png");
  TCanvas* c3 = plt.Hist1d(l1dist, 700, 500);
  // plt.AddStats(c3, l1dist, 1);
  plt.SaveAs(c3, fname, "_l1id.png");
  TCanvas* c4 = plt.Hist1d(tot, 700, 500);
  // plt.AddStats(c4, tot, 1);
  plt.SaveAs(c4, fname, "_tot.png");  
  TCanvas* c5 = plt.Hist2dLogz(HitperTrig, 700, 500);
  plt.SaveAs(c5, fname, "_hetpertrig.png");  
}




