#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gSystem.Load("libRooFit.so" ) # for bindFunction
#https://root.cern.ch/root/htmldoc/tutorials/roofit/rf105_funcbinding.C.html

import os,sys, math
from array import array

import MNTriggerStudies.MNTriggerAna.Util

from  RooDSHelper import getSummedRooDS, reweighDS

# I hate myself...
#bins = [x for x in xrange(35, 81,5)]
bins = [x for x in xrange(30, 81,5)]
bins.append(100)
bins.append(120)
bins.append(140)
binsArray = array('d',bins)
hData = ROOT.TH1F("dataa", "dataa", len(binsArray)-1, binsArray)
#hData = ROOT.TH1F("dataa", "dataa", 100, 35, 135)
hData.Sumw2()
hMCbase = hData.Clone()
globalMC = None

def doMinuitFit(ofile, dsData, dsMC, lumi):
    c = ROOT.TCanvas()
    hData.Reset()
    dsData[0].fillHistogram(hData, ROOT.RooArgList(dsData[1]["leadPt"]))
    hData.Scale(1./lumi)
    global globalMC
    globalMC = dsMC


    # initial fit for starting values
    hMC = hMCbase.Clone("MC")
    dsMC[0].fillHistogram(hMC, ROOT.RooArgList(dsMC[1]["leadPt"]))
    hData2MC = hData.Clone("data2mc")
    hData2MC.Divide(hMC)

    #fitF = ROOT.TF1("ptHatW","[0]+[1]*(x**[2])", 0, 1000000);
    #fitF = ROOT.TF1("ptHatW","[0]+[1]*x", 0, 1000000);
    fitF = ROOT.TF1("ptHatW","[0]+[1]/x", 0, 1000000);
    #fitF = ROOT.TF1("ptHatW","[0]+[1]*exp(x/[2])", 0, 1000000);#
    #     linear = ROOT.RooFormulaVar("lin", "lin", "a1+a2*(qScale/a3)", args)


    fitF.SetParameter(0, 0.)
    fitF.SetParameter(1, 1.)
    #fitF.SetParameter(2, -10) #xxx
    hData2MC.Fit("ptHatW")
    hData2MC.Draw()
    c.Print("~/tmp/steps/start_"+dsMC[0].GetName()+".png")

    
    a1Start, a1err = fitF.GetParameter(0), fitF.GetParError(0)
    a2Start, a2err = fitF.GetParameter(1), fitF.GetParError(1)
    #a3Start, a3err = fitF.GetParameter(2), fitF.GetParError(2) # xxx


    # setup minuit
    gMinuit = ROOT.TMinuit(5)
    gMinuit.SetFCN( fcn )

    arglist = array( 'd', 10*[0.] )
    ierflg = ROOT.Long(1982)

    arglist[0] = 1
    gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )

    # Set starting values and step sizes for parameters
    # Best linear, herwig: Call: 63 0.495972878319 0.0115689236499 chisq 192.329885935
    # Best a+b/x,
    #   herwig (my chi2, no lowPT):     Call: 142 1.74440199586 -27.5599163958 chisq 28.5523011508
    #   herwig (my chi2, lowPT): Call: 142 1.74440199586 -27.5599163958 chisq 28.5523011508 # same vals?
    #   herwig (root chi2, WW, no lowPT) : Call: 65 2.00594999924 -33.8966266938 chisq 112.237294756
    #   herwig (root chi2, UW, no lowPT) : Call: 117 2.11427928202 -33.999978712 chisq 66.8756343924


    # best a+bx**c, herwig: Call: 30 -8.19785565098 6.92050519408 0.0768261455595 chisq 155.637202664

    # best exp so far: herwig : Call: 191 0.662748696815 -1.28651289298 -148.376339102 chisq 157.633606971


    #vstart = array( 'd', ( a1Start,  a2Start) )
    vstart = array( 'd', ( 2,  -35) )
    step   = array( 'd', ( 0.1, 1 ) )
    #vstart = array( 'd', ( a1Start,  a2Start, a3Start) ) # xxx
    #vstart = array( 'd', ( 0.2,  -0.5, -150.) )
    #step   = array( 'd', ( 0.1, 0.1, 0.01 ) )
    #step   = array( 'd', ( a1err, a2err ) )
    #step   = array( 'd', ( a1err, a2err, a3err ) ) # xxx
    #step   = array( 'd', ( 0.02, 0.02, 5 ) )
    gMinuit.mnparm( 0, "a1", vstart[0], step[0], 0, 0, ierflg )
    gMinuit.mnparm( 1, "a2", vstart[1], step[1], 0, 0, ierflg )
    #gMinuit.mnparm( 2, "a3", vstart[2], step[2], 0, 0, ierflg ) # xxx

    # 
    #gMinuit.DefineParameter( 0, "a1", vstart[0], step[0], -100, 100)
    #gMinuit.DefineParameter( 1, "a2", vstart[1], step[1], -100, 100)
    #gMinuit.DefineParameter( 3, "a3", vstart[2], step[2], -2, 0)


    # Now ready for minimization step
    arglist[0] = 500 # max calls 
    arglist[1] = 1000.  # tolerance - how far from minimum
    gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )

    # Print results
    amin, edm, errdef = ROOT.Double(0.18), ROOT.Double(0.19), ROOT.Double(0.20)
    nvpar, nparx, icstat = ROOT.Long(1983), ROOT.Long(1984), ROOT.Long(1985)
    gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )


    val, err = ROOT.Double(0), ROOT.Double(0)
    for i in xrange(len(vstart)):
        gMinuit.GetParameter(i, val, err)
        fitF.SetParameter(i, val)

    ofile.WriteTObject(fitF)



cnt = 0
lastTime = None
import time
def sinceLast(msg):
    return
    global lastTime
    #cur = time.clock()
    cur = time.time()
    if not lastTime:
        lastTime = cur

    print "T", msg, cur-lastTime
    lastTime = cur




def fcn( npar, gin, f, par, iflag ):
    sinceLast("fcn start")
    global cnt
    cnt +=1
    # get weighted MC ds
    global globalMC
    vars = globalMC[1]
    #localMCds = globalMC[0].Clone()
    baseWeight = "weight" # yuck, Q&D
    a1 = ROOT.RooRealVar("a1","a1", par[0])
    a2 = ROOT.RooRealVar("a2","a2", par[1])
    #a3 = ROOT.RooRealVar("a3","a3", par[2]) # xxx
    #args = ROOT.RooArgList(vars["qScale"], a1, a2, a3) # xxx
    args = ROOT.RooArgList(vars["qScale"], a1, a2)
    #linear = ROOT.RooFormulaVar("lin", "lin", "a1+a2*qScale", args)
    linear = ROOT.RooFormulaVar("lin", "lin", "(a1+a2/qScale)*(qScale>0.01)", args)
    #linear = ROOT.RooFormulaVar("lin", "lin", "(a1+a2*(qScale**a3))*(qScale>0.01)", args)
    #linear = ROOT.RooFormulaVar("lin", "lin", "a1+a2*exp(qScale/a3)", args)

    newweight = ROOT.RooFormulaVar("w"+str(cnt), "ww", baseWeight+"*lin"  , ROOT.RooArgList(vars[baseWeight], linear))

    sys.stdout.flush()

    sinceLast("fcn init donw, now reweigh")
    wds = reweighDS(globalMC[0], "neww", newweight) # 

    # fill MC histograms
    hMC = hMCbase.Clone("MC")
    sinceLast("fcn rew done, now fill")
    wds.fillHistogram(hMC, ROOT.RooArgList(vars["leadPt"]))
    del wds
    #globalMC[0].fillHistogram(hMC, ROOT.RooArgList(vars["leadPt"]))

    sinceLast("fcn fill done, now plots")
    c = ROOT.TCanvas()
    hMC.Draw()
    hMC.SetLineColor(2)

    hData.Draw("SAME")
    newMax = 1.05*max(hMC.GetMaximum(), hData.GetMaximum())
    hMC.SetMaximum(newMax)
    #hData.SetMaximum(newMax)
    c.Print("~/tmp/steps/"+globalMC[0].GetName()+"_"+str(cnt)+".png")

    hRatio = hData.Clone()
    hRatio.Divide(hMC)
    hRatio.Draw()
    hRatio.SetMaximum(1.5)
    c.Print("~/tmp/steps/ratio_"+globalMC[0].GetName()+"_"+str(cnt)+".png")

    # get chi2
    sinceLast("fcn plots dons, now chi2")
    #'''
    chisq, delta = 0., 0.
    for i in xrange(1, hMC.GetNbinsX()+1):
        errData = hData.GetBinError(i)
        errMC =   hMC.GetBinError(i)
        #print "B", i, errData, errMC, 
        err = math.sqrt(errData*errData+errMC*errMC)
        if err > 0:
            delta = (hData.GetBinContent(i)-hMC.GetBinContent(i))/err
            chisq += delta*delta
    '''    
    #chisq = hData.Chi2Test(hMC, "WW OF CHI2") # overflow bin included in comparison
    #chisq = hData.Chi2Test(hMC, "WW CHI2") 
    #chisq = hData.Chi2Test(hMC, "UW CHI2") 
    # '''
    f[0] = chisq
    #print "Call:", cnt, par[0], par[1], par[2], "chisq", chisq
    print "Call:", cnt, par[0], par[1], "chisq", chisq

    
    sinceLast("fcn end")

def doBaselineFit(ofile, dsData, dsMC, lumi):
    c = ROOT.TCanvas()
    hData.Reset()
    dsData[0].fillHistogram(hData, ROOT.RooArgList(dsData[1]["leadPt"]))
    hData.Scale(1./lumi)

    hMC = hMCbase.Clone("MC")
    dsMC[0].fillHistogram(hMC, ROOT.RooArgList(dsMC[1]["leadPt"]))
    hMC.Draw()
    hMC.SetLineColor(2)
    hData.Draw("SAME")
    c.Print("~/tmp/ttt.png")
    
    hData2MC = hData.Clone("data2mc")
    hData2MC.Divide(hMC)

    fitF = ROOT.TF1("ptHatW","[0]/x + [1]", 0, 1000000);
    fitF.SetParameter(0, 0.)
    fitF.SetParameter(1, 1.)
    hData2MC.Fit("ptHatW")

    ofile.WriteTObject(hData2MC)
    ofile.WriteTObject(hData)
    ofile.WriteTObject(hMC)
    ofile.WriteTObject(fitF)




def main():
    dataDSNames = ["JetMETTau-Run2010A-Apr21ReReco-v1", "Jet-Run2010B-Apr21ReReco-v1", "JetMET-Run2010A-Apr21ReReco-v1"]
    data = getSummedRooDS("data", "treesForPTHatReweighing.root", dataDSNames)
    lumi = 0.
    sampleList=MNTriggerStudies.MNTriggerAna.Util.getAnaDefinition("sam")
    for s in dataDSNames:
        lumi += sampleList[s]["lumiJet15"]

    print "Lumi:", lumi

    #todoQCDNames = ["QCD_Pt-15to3000_TuneZ2star_Flat_HFshowerLibrary_7TeV_pythia6", "QCD_Pt-15to1000_TuneEE3C_Flat_7TeV_herwigpp"]
    todoQCDNames = ["QCD_Pt-15to1000_TuneEE3C_Flat_7TeV_herwigpp",]
    #todoQCDNames = ["QCD_Pt-15to3000_TuneZ2star_Flat_HFshowerLibrary_7TeV_pythia6"]

    outFile = ROOT.TFile("ptHatWeighters.root", "recreate")
    for t in todoQCDNames:
        xxx = outFile.mkdir(t)
        dMC = getSummedRooDS(t, "treesForPTHatReweighing.root", [t], "weight")
        #dMC = getSummedRooDS(t, "treesForPTHatReweighing.root", [t])

        #doBaselineFit(xxx, data, dMC, lumi)
        doMinuitFit(xxx, data, dMC, lumi)

#       leadEta
#       leadPt
#       qScale








if __name__ == "__main__":
    main()