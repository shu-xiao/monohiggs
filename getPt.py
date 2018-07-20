#!/bin/python
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis, TH1F, TH1, TString, TLegend
from array import array
from ROOT import TColor
import os
import csv

hApath = 'events_presys.lhe'
hApathList = ['Zp2HDM_bb_MZp600_MA0300_tanbeta1_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0300_tanbeta1_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0500_tanbeta1_0_MDM100.lhe']
hApathList_5 = ['Zp2HDM_bb_MZp600_MA0300_tanbeta5_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0300_tanbeta5_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0500_tanbeta5_0_MDM100.lhe']
legtext = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=1.0']
legtext_5 = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=5.0']
hA_files = glob.glob(hApath) 
class fourVect():
    def __init__(self,px=0,py=0):
        self.px = px
        self.py = py
        self.pt = (px**2+py**2)**0.5


def getPtList(name):
    vList = []
    try:
        with open(name) as f:
            for line in f:
                if line.find("25")>0 and line.find('0.12500000000E+03')>0:
                    temlist = filter(None,line.split(" "))
                    vList.append(fourVect(float(temlist[6]),float(temlist[7])))
    
    except IOError as exc:
        if exc.errno != errno.EISDIR: 
            raise

    return vList

def main():
    gStyle.SetOptStat(0)
    c1 = TCanvas('c1','c1',3)
    c1.SetLeftMargin(0.12)
    h_frame = TH1F('frame','',50,0,1000)
    h_frame.SetXTitle('higgs P_{T} (GeV)')
    h_frame.SetYTitle('A.U.')
    h_frame.SetMaximum(4000)

    h_higgsPt = TH1F('h_higgsPt','h_higgsPt',50,0,1000)
    h_higgsPtList = []
    for i in range(6): 
        h_higgsPtList.append(TH1F('h_higgsPt_'+str(i),'',50,0,1000))
        h_higgsPtList[i].SetLineWidth(2)
    ## test code 
    ivVectList = getPtList(hApath)
    for fourV in ivVectList:
        h_higgsPt.Fill(fourV.pt)

    
    ## loop all combination
    leg = TLegend(0.4,0.6,0.9,0.9)
    for i in range(3):
        ivVectList = getPtList(hApathList[i])
        h_higgsPtList[i].SetLineColor(87+4*i)
        leg.AddEntry(h_higgsPtList[i],legtext[i])
        for fourV in ivVectList:
            h_higgsPtList[i].Fill(fourV.pt)
    
    for i in range(3):
        ivVectList = getPtList(hApathList_5[i])
        h_higgsPtList[i+3].SetLineColor(61+4*i)
        leg.AddEntry(h_higgsPtList[i+3],legtext_5[i])
        for fourV in ivVectList:
            h_higgsPtList[i+3].Fill(fourV.pt)
    
    h_frame.Draw('hist')
    #h_higgsPt.Draw('histsame')
    for i in range(6): h_higgsPtList[i].Draw('histsame')
    leg.Draw()
    c1.Print('test.pdf')
if __name__ == "__main__":
    main()
