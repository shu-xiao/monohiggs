#!/bin/python
import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D, TGaxis, TH1F, TH1, TString, TLegend
from ROOT import TColor, gPad, TLatex
from array import array
import os
import csv



def main():
    gStyle.SetOptStat(0)
    zplist = [600,600,1200,1200,2000,2000]
    a0list = [300,400,300,500,300,600]
    c1 = TCanvas('c1','c1',3)
    gPad.SetTickx()
    gPad.SetTicky()
    c1.SetLeftMargin(0.12)
    h_frame = TH1F('frame','',60,0,1200)
    h_frame.SetXTitle('P^{miss}_{T} (GeV)')
    h_frame.SetYTitle('Arbitrary units')
    h_frame.SetMaximum(0.3)

    h_higgsPt = TH1F('h_higgsPt','h_higgsPt',60,0,1200)
    h_higgsPtList = []
    rootfilelist = []
    for i in range(6):
        fName = 'rootFile/higgsPt_MZp'+str(zplist[i])+'_MA0'+str(a0list[i])+'.root'
        rootfile = TFile(fName)
        rootfilelist.append(rootfile)
    
    colorList = [61,95,65,91,69,87] 
    for i in range(6):
        hist = rootfilelist[i].Get('h_higgsPt')
        hist.SetName('h_higgsPt_MZp'+str(zplist[i])+'_MA0'+str(a0list[i]))
        h_higgsPtList.append(hist)
        h_higgsPtList[i].SetLineWidth(2)
        h_higgsPtList[i].SetLineColor(colorList[i])
    
    info_bar = TLatex(0,0.305,'CMS')
    info_bar_3 = TLatex(700,0.15,'#font[42]{tan#beta=1.0}')
    info_bar_2 = TLatex(1200,0.305,'35.9 fb^{-1} (13 TeV)')
    info_bar.SetTextSize(0.03)
    info_bar_2.SetTextSize(0.03)
    info_bar_3.SetTextSize(0.04)
    info_bar_2.SetTextAlign(31)
    leg = TLegend(0.32,0.57,0.87,0.87)
    leg.SetBorderSize(0)
    for j in range(3):
        i = 2*j
        text = 'M_{Z\'} = '+str(zplist[i])+' GeV, M_{A} = '+str(a0list[i])+' GeV'
        leg.AddEntry(h_higgsPtList[i],text)
    
    for j in range(3):
        i = 2*j+1
        text = 'M_{Z\'} = '+str(zplist[i])+' GeV, M_{A} = '+str(a0list[i])+' GeV'
        leg.AddEntry(h_higgsPtList[i],text)
    
    h_frame.Draw('hist')
    for i in range(6): h_higgsPtList[i].DrawNormalized('histsame')
    leg.Draw()
    info_bar.Draw()
    info_bar_2.Draw()
    info_bar_3.Draw()
    c1.Print('Zp2HDM_higgsPt_new.pdf')
    
    '''
    f = TFile('rootFile/Zp2HDM_missPt_new.root','recreate')
    for i in range(6):
        h_higgsPtList[i].SetLineColor(1)
        h_higgsPtList[i].Write()
    
    f.Close()
    '''


if __name__ == "__main__":
    main()
