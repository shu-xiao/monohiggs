#include "/home/shuxiao/BZntuple/gen2HDMsample/genMatch.C"
#include "/home/shuxiao/BZntuple/reco4jets/2HDMfullSimFile/untuplizer.h"
using namespace std;
void getGenPt(string inputFile) {
    TString Zpmass=gSystem->GetFromPipe(Form("file=%s; test1=${file##*_MZp}; test=${test1%%_MA0*.root}; echo \"${test}\"",inputFile.data()));
    TString A0mass=gSystem->GetFromPipe(Form("file=%s; test1=${file##*MA0}; test=${test1%%.root}; echo \"${test}\"",inputFile.data()));
    
    string fName = Form("rootFile/higgsPt_MZp%d_MA0%d.root",Zpmass.Atoi(),A0mass.Atoi());
    TFile *fout = new TFile(fName.data(),"recreate");
    TH1F *h_higgsPt = new TH1F("h_higgsPt","h_higgsPt",60,0,1200);
    TreeReader data(inputFile.data());
    for(Long64_t jEntry=0; jEntry<data.GetEntriesFast() ;jEntry++){

        if (jEntry %2000 == 0) fprintf(stderr, "Processing event %lli of %lli\n", jEntry + 1, data.GetEntriesFast());
        data.GetEntry(jEntry);
        TClonesArray* genParP4 = (TClonesArray*) data.GetPtrTObject("genParP4");
        int *genMomParId, *genParId;
        genMomParId= data.GetPtrInt("genMomParId");
        genParId= data.GetPtrInt("genParId");
        int Hindex[2]={-1,-1}, A0index[2]={-1,-1};
        vector<TLorentzVector*> genParIndexList;
        // match higgs
        for(int ij=0; ij < 30; ij++) {
            //TLorentzVector* thisParP4 = (TLorentzVector*)genParP4->At(ij);
            if (abs(genParId[ij])!=5) continue;
            //if(upeff && thisParP4->Pt()<30) continue;
            //if(upeff && fabs(thisParP4->Eta())>2.4) continue;
            
            if (genMomParId[ij]==25 && Hindex[0]<0) Hindex[0] = ij;
            else if (genMomParId[ij]==25 && Hindex[1]<0) Hindex[1] = ij;
            
            if (genMomParId[ij]==28 && A0index[0]<0) A0index[0] = ij;
            else if (genMomParId[ij]==28 && A0index[1]<0) A0index[1] = ij;
        } // end of outer loop jet
        for (int i=0;i<2;i++) genParIndexList.push_back((TLorentzVector*)genParP4->At(Hindex[i]));
        TLorentzVector higgsJet = *genParIndexList[0] + *genParIndexList[1];
        h_higgsPt->Fill(higgsJet.Pt());
    }
    h_higgsPt->Write();
    fout->Close();
}
