#!/usr/bin/env python

# to be used with SmallXAnaVersion=CommonFSQFramework.Core.samples.Samples_DiJet_20140122_MN2010
import CommonFSQFramework.Core.ExampleProofReader

import sys, os, time
import math
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import edm

from array import *

# EX 8.0
from  CommonFSQFramework.Core.BetterJetGetter import BetterJetGetter


class SingleJet2015(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init( self):
        self.hist = {}
        self.hist["numGenTracks"] =  ROOT.TH1F("numGenTracks",   "numGenTracks",  100, -0.5, 99.5)

	self.hist["deltaEta"] =  ROOT.TH1F("deltaEta",   "deltaEta", 48,0,9.4)
	self.hist["deltaPt"] = ROOT.TH1F("deltaPt","deltaPt",400,0,100)
	self.hist["deltaPhi"] = ROOT.TH1F("deltaPhi","deltaPhi",200,-4,4)
	self.hist["hprof_cos"] = ROOT.TProfile("hprof_cos","Profile of C_{1} versus #Delta#eta",15,0,9.4);

        # EX3
        self.hist["numVtx"] =  ROOT.TH1F("numVtx",   "numVtx",  5, -0.5, 4.5)
        self.hist["jetPT"] =  ROOT.TH1F("jetPT",   "jetPT",  100, 0, 100)

        # EX9 
        self.hist["jetBelowEta3PT"] =  ROOT.TH1F("jetBelowEta3PT", "jetBelowEta3PT",  100, 0, 100)
        self.hist["jetBelowEta3Eta"] =  ROOT.TH1F("jetBelowEta3Eta",   "jetBelowEta3Eta" ,  100, -5, 5)
        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        # EX 8.0
        self.jetGetter = BetterJetGetter("PFAK4CHS") 

    def analyze(self):
        # ex 4.5
        #if self.isData and self.fChain.jet15 < 0.5:
        #    return 

        if self.isData and self.fChain.trgDiPFJet15_FBEta2 < 0.5:
            return 

        weight = 1.
        # EX 6.
        #if not self.isData:
        #    weight *= self.fChain.genWeight

        num = 0

        # genTracks
        #num = self.fChain.genTracks.size()
        #print num
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(num, weight)

        # EX2.0
        #print "vtx", self.fChain.ngoodVTX

        # EX3.0
        #self.hist["numVtx"].Fill(self.fChain.ngoodVTX, weight)

        # EX5.0
	
	jets_Ana = []

        for i in xrange(self.fChain.PFAK4CHSpt.size()):
            pt = self.fChain.PFAK4CHSpt.at(i)
            if pt < 35: continue
            self.hist["jetPT"].Fill(pt, weight)
	    jets_Ana.append(i)


	if len(jets_Ana)>1:

    	    max_deta = 0

	    for i in xrange(len(jets_Ana)):
	        for j in xrange(len(jets_Ana)):
	            if j>i:
		        deta =  self.fChain.PFAK4CHSeta.at(jets_Ana[i])-self.fChain.PFAK4CHSeta.at(jets_Ana[j])
			if deta < 0:
			    deta = -deta
		        if deta > max_deta:
			    max_deta = deta
			    jet1_eta = self.fChain.PFAK4CHSeta.at(jets_Ana[i])
			    jet1_pt = self.fChain.PFAK4CHSpt.at(jets_Ana[i])
			    jet1_phi = self.fChain.PFAK4CHSphi.at(jets_Ana[i])
                            jet2_eta = self.fChain.PFAK4CHSeta.at(jets_Ana[j])
                            jet2_pt = self.fChain.PFAK4CHSpt.at(jets_Ana[j])
                            jet2_phi = self.fChain.PFAK4CHSphi.at(jets_Ana[j])
	    #print max_deta
	    
	    delta_pt = math.fabs(jet1_pt - jet2_pt)
	    Dphi = 2*math.atan(math.tan((jet1_phi - jet2_phi)/2.));
            cosDphi = math.cos(math.pi-Dphi);
            cos2Dphi = math.cos(2.*(math.pi-Dphi));

            if (Dphi<0):
	        Dphi=Dphi+math.pi
      	    else:
		if (Dphi>0):
		    Dphi=Dphi-math.pi
	    
	    self.hist["deltaEta"].Fill(max_deta,weight)
            self.hist["deltaPt"].Fill(delta_pt,weight)
            self.hist["deltaPhi"].Fill(Dphi,weight)
            self.hist["hprof_cos"].Fill(deta,cosDphi,weight)


        # EX 8.0
        #self.jetGetter.newEvent(self.fChain)
        #print "New event!"
        #for j in self.jetGetter.get("_central"):
         #    if j.pt()<35.: continue
             #print "A jet: ", j.pt(), j.eta()


        # EX 9.0
        #for j in self.jetGetter.get("_central"):
           #  if j.pt()<35.: continue
            # if abs(j.eta())>3.: continue
            # self.hist["jetBelowEta3Eta"].Fill(j.eta(), weight)
            # self.hist["jetBelowEta3PT"].Fill(j.pt(), weight)


        return 1

    def finalize(self):
        print "Finalize:"
       # normFactor = self.getNormalizationFactor()
        # exercise A.2
        #  this is the lumi for jet15 trigger in JetMETtau
        #if self.isData:
         #   print "Expected norm factor is 1. Got", normFactor
          #  print "Changeing norm factor to have properly normalized data histo"
           # normFactor = 1/0.013781

#        print "  applying norm", normFactor
        #for h in self.hist:
         #   self.hist[h].Scale(normFactor)

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = None # run through all
    maxFilesMC = None # run through all ffiles found
    maxFilesData = None # same
    nWorkers = None # Use all cpu cores

    # debug config:
    # Run printTTree.py alone to get the samples list

    # Exercise A.1
    sampleList = []
    #sampleList.append("QCD_Pt-15to3000_TuneZ2star_Flat_HFshowerLibrary_7TeV_pythia6")
    #sampleList.append("QCD_Pt-15to1000_TuneEE3C_Flat_7TeV_herwigpp")
    #sampleList.append("JetMETTau-Run2010A-Apr21ReReco-v1")
    
    sampleList.append("data_FSQJets3")
    maxFilesMC = 1
    #maxFilesData = 1
    maxNevents = -1
    nWorkers = 16


    slaveParams = {}
    slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    SingleJet2015.runAll(treeName="JetTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           maxNevents = maxNevents,
           nWorkers=nWorkers,
           outFile = "plotsSingleJet_2016.root" )
