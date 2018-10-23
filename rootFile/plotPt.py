#!/bin/python
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis, TH1F, TH1, TString, TLegend
from ROOT import TColor, gPad, TLatex
from array import array
import os
import csv

#hApath = 'events_presys.lhe'
legtext = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=1.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=1.0']
legtext_5 = ['M_{Zp}=600 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=300 GeV, tan#beta=5.0','M_{Zp}=1400 GeV, M_{A0}=500 GeV, tan#beta=5.0']
histName_zp2HDM = ['missPt_MZp600_MA0300_tb1','missPt_MZp1400_MA0300_tb1','missPt_MZp1400_MA0500_tb1','missPt_MZp600_MA0300_tb5','missPt_MZp1400_MA0300_tb5','missPt_MZp1400_MA0500_tb5']

legtext_bar = ['M_{Zp}=1000 GeV,M_{#chi}=500 GeV','M_{Zp}=1000 GeV,M_{#chi}=100 GeV','M_{Zp}=1000 GeV,M_{#chi}=1 GeV','M_{Zp}=500 GeV,M_{#chi}=1 GeV',\
        'M_{Zp}=100 GeV,M_{#chi}=1 GeV','M_{Zp}=10 GeV,M_{#chi}=1 GeV']
histName_bar = ['missPt_MZp1000_MDM500','missPt_MZp1000_MDM100','missPt_MZp1000_MDM1','missPt_MZp500_MDM1','missPt_MZp100_MDM1','missPt_MZp10_MDM1']
#hA_files = glob.glob(hApath) 

def main():
    gStyle.SetOptStat(0)
    c1 = TCanvas('c1','c1',3)
    gPad.SetTickx()
    gPad.SetTicky()
    c1.SetLeftMargin(0.12)
    h_frame = TH1F('frame','',50,0,1000)
    h_frame.SetXTitle('P^{miss}_{T} [GeV]')
    h_frame.SetYTitle('Arbitrary units')
    h_frame.SetMaximum(0.4)
    info_zp2HDM = TLatex(0,0.405,'CMS')
    info_zp2HDM_2 = TLatex(1000,0.405,'35.9 fb^{-1} (13 TeV)')
    info_zp2HDM.SetTextSize(0.03)
    info_zp2HDM_2.SetTextSize(0.03)
    info_zp2HDM_2.SetTextAlign(31)
    
    # Zp-2HDM
    h_higgsPtList = []
    f = TFile('Zp2HDM_missPt.root')
    for i in range(6): 
        hist = TH1F()
        hist = f.Get(histName_zp2HDM[i])
        h_higgsPtList.append(hist)
    
    leg = TLegend(0.32,0.57,0.87,0.87)
    leg.SetBorderSize(0)
    for i in range(3):
        h_higgsPtList[i].SetLineColor(87+4*i)
        leg.AddEntry(h_higgsPtList[i],legtext[i])
    
    for i in range(3):
        h_higgsPtList[i+3].SetLineColor(61+4*i)
        leg.AddEntry(h_higgsPtList[i+3],legtext_5[i])
    
    h_frame.Draw('hist')
    for i in range(6): h_higgsPtList[i].DrawNormalized('histsame')
    leg.Draw()
    info_zp2HDM.Draw()
    info_zp2HDM_2.Draw()
    c1.Print('Zp2HDM_higgsPt.pdf')
    f.Close()
    
    ## Baryonic
    h_frame.SetMaximum(0.25)
    h_frame.SetAxisRange(0., 750.,"X")
    leg.Clear() 
    info_bar = TLatex(0,0.255,'CMS')
    info_bar_2 = TLatex(750,0.255,'35.9 fb^{-1} (13 TeV)')
    info_bar.SetTextSize(0.03)
    info_bar_2.SetTextSize(0.03)
    info_bar_2.SetTextAlign(31)

    kOrange = 800
    colorList = [kOrange-4,kOrange-1,kOrange+3,70,65,55]
    h_higgsPt_BarList = []
    f = TFile('BaryonicZp_missPt.root')
    for i in range(6): 
        hist = TH1F()
        hist = f.Get(histName_bar[i])
        h_higgsPt_BarList.append(hist)
    
    for i in range(6):
        #h_higgsPt_BarList[i].SetLineColor(93-6*i)
        h_higgsPt_BarList[i].SetLineColor(colorList[i])
        leg.AddEntry(h_higgsPt_BarList[i],legtext_bar[i])

    h_frame.Draw('hist')
    for i in range(5,-1,-1):h_higgsPt_BarList[i].DrawNormalized('histsame')
    leg.Draw()
    info_bar.Draw()
    info_bar_2.Draw()
    c1.Print('Baryonic_higgsPt.pdf')
    f.Close()


if __name__ == "__main__":
    main()
