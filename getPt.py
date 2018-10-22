#!/bin/python
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis, TH1F, TH1, TString, TLegend
from ROOT import TColor, gPad
from array import array
import os
import csv

#hApath = 'events_presys.lhe'
hApathList = ['Zp2HDM_bb_MZp600_MA0300_tanbeta1_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0300_tanbeta1_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0500_tanbeta1_0_MDM100.lhe']
hApathList_5 = ['Zp2HDM_bb_MZp600_MA0300_tanbeta5_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0300_tanbeta5_0_MDM100.lhe','Zp2HDM_bb_MZp1400_MA0500_tanbeta5_0_MDM100.lhe']
legtext = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=1.0']
legtext_5 = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=5.0']
histName_zp2HDM = ['missPt_MZp600_MA0300_tb1','missPt_MZp1400_MA0300_tb1','missPt_MZp1400_MA0500_tb1','missPt_MZp600_MA0300_tb5','missPt_MZp1400_MA0300_tb5','missPt_MZp1400_MA0500_tb5']

hApath_barList = ['ZpBaryonic_bb_MZp1000_gq25_MDM500.lhe','ZpBaryonic_bb_MZp1000_gq25_MDM100.lhe','ZpBaryonic_bb_MZp1000_gq25_MDM1.lhe',\
        'ZpBaryonic_bb_MZp500_gq25_MDM1.lhe','ZpBaryonic_bb_MZp100_gq25_MDM1.lhe','ZpBaryonic_bb_MZp10_gq25_MDM1.lhe']
legtext_bar = ['M_{Zp}=1000 GeV,M_{#chi}=500 GeV','M_{Zp}=1000 GeV,M_{#chi}=100 GeV','M_{Zp}=1000 GeV,M_{#chi}=1 GeV','M_{Zp}=500 GeV,M_{#chi}=1 GeV',\
        'M_{Zp}=100 GeV,M_{#chi}=1 GeV','M_{Zp}=10 GeV,M_{#chi}=1 GeV']
histName_bar = ['missPt_MZp1000_MDM500','missPt_MZp1000_MDM100','missPt_MZp1000_MDM1','missPt_MZp500_MDM1','missPt_MZp100_MDM1','missPt_MZp10_MDM1']
#hA_files = glob.glob(hApath) 
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
    gPad.SetTickx()
    gPad.SetTicky()
    c1.SetLeftMargin(0.12)
    h_frame = TH1F('frame','',50,0,1000)
    h_frame.SetXTitle('P^{miss}_{T} (GeV)')
    h_frame.SetYTitle('Arbitrary units')
    h_frame.SetMaximum(0.4)

    h_higgsPt = TH1F('h_higgsPt','h_higgsPt',50,0,1000)
    h_higgsPtList = []
    for i in range(6): 
        h_higgsPtList.append(TH1F(histName_zp2HDM[i],'',50,0,1000))
        h_higgsPtList[i].SetLineWidth(2)
    h_higgsPt_BarList = []
    for i in range(6):
        h_higgsPt_BarList.append(TH1F(histName_bar[i],'',40,0,800))
        h_higgsPt_BarList[i].SetLineWidth(2)
    ## test code 
    '''
    ivVectList = getPtList(hApath)
    for fourV in ivVectList:
        h_higgsPt.Fill(fourV.pt)
    '''
    
    ## loop all combination
    leg = TLegend(0.32,0.57,0.87,0.87)
    leg.SetBorderSize(0)
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
    for i in range(6): h_higgsPtList[i].DrawNormalized('histsame')
    leg.Draw()
    c1.Print('Zp2HDM_higgsPt.pdf')
    
    ## Baryonic
    h_frame.SetMaximum(0.25)
    h_frame.SetAxisRange(0., 750.,"X")
    leg.Clear() 
    for i in range(6):
        ivVectList = getPtList('BaryonicFile/'+hApath_barList[i])
        h_higgsPt_BarList[i].SetLineColor(90-6*i)
        leg.AddEntry(h_higgsPt_BarList[i],legtext_bar[i])
        for fourV in ivVectList:
            h_higgsPt_BarList[i].Fill(fourV.pt)

    h_frame.Draw('hist')
    for i in range(5,-1,-1):h_higgsPt_BarList[i].DrawNormalized('histsame')
    leg.Draw()
    c1.Print('Baryonic_higgsPt.pdf')
    f = TFile('rootFile/Zp2HDM_missPt.root','recreate')
    for i in range(6):
        h_higgsPtList[i].SetLineColor(1)
        h_higgsPtList[i].Write()
    
    f.Close()
    
    f = TFile('rootFile/BaryonicZp_missPt.root','recreate')
    for i in range(6):
        h_higgsPt_BarList[i].SetLineColor(1)
        h_higgsPt_BarList[i].Write()

    f.Close()


if __name__ == "__main__":
    main()
