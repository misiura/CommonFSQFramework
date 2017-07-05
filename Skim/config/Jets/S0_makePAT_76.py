import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

process = cms.Process('Treemaker')

## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
#process = cms.Process('Treemaker')

process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.coreTools import runOnData



process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching



## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)

#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.coreTools import runOnData

process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching

if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on MC"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: 
	print "Disabling MC-specific features for sample",s
	runOnData(process)
        removeMCMatching(process, ['All'])



#runOnData(process)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/data/Run2015C_25ns/FSQJets3/AOD/16Dec2015-v1/50000/062D1243-AEAF-E511-A5A2-549F35AD8BF0.root')

 fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/mc/RunIIFall15MiniAODv2/QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp/MINIAODSIM/PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1/00000/1A98EFF8-0C2A-E611-9C07-00259073E3D4.root')

# fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/data/Run2015C_25ns/FSQJets3/MINIAOD/16Dec2015-v1/50000/0E13C771-AFAF-E511-AA03-002618943914.root')
#fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/mc/RunIIFall15MiniAODv2/QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp/MINIAODSIM/PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1/00000/1A98EFF8-0C2A-E611-9C07-00259073E3D4.root')
)
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

#test
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

from PhysicsTools.PatAlgos.tools.metTools import addMETCollection
#addMETCollection(process, labelName='patMETCalo', metSource='met')
addMETCollection(process, labelName='patMETPF', metSource='pfMetT1')
#addMETCollection(process, labelName='patMETTC', metSource='tcMet') # FIXME: removed from RECO/AOD; needs functionality to add to processing

## uncomment the following line to add different jet collections
## to the event content
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

## uncomment the following lines to add ak4PFJetsCHS to your PAT output
labelAK4PFCHS = 'selectedPatJetsAK4PFCHS'
#labelAK4PFCHS = 'AK4PFCHS'
postfixAK4PFCHS = 'Copy'
addJetCollection(
   process,
   postfix   = postfixAK4PFCHS,
   labelName = labelAK4PFCHS,
   jetSource = cms.InputTag('ak4PFJetsCHS'),
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-2')
   )
process.out.outputCommands.append( 'drop *_selectedPatJets%s%s_caloTowers_*'%( labelAK4PFCHS, postfixAK4PFCHS ) )

# Here starts the CFF specific part
import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)

# GT customization
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

process.JetTree = cms.EDAnalyzer("CFFTreeProducer")
import CommonFSQFramework.Core.JetViewsConfigs
process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["JetViewPFAK4CHS"]))

import CommonFSQFramework.Core.VerticesViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs

process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
if isData: process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["DiPFJet15"]))


#process = CommonFSQFramework.Core.customizePAT.addPath(process, runOnData(process))
#process.PATprod = cms.Path(process.patCandidates*process.selectedPatCandidates)

#process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PATprod)

process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetTree)

#from PhysicsTools.PatAlgos.tools.coreTools import *
#restrictInputToAOD(process, ['All'])


#if "TMFSampleName" not in os.environ:
#    print "TMFSampleName not found, assuming we are running on MC"
#else:
#    s = os.environ["TMFSampleName"]
#    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
#    isData =  sampleList[s]["isData"]
#    if isData:
#        print "Disabling MC-specific features for sample",s
#        runOnData(process)
#        removeMCMatching(process, ['All'])

