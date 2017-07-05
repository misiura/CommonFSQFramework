from WMCore.Configuration import Configuration
config = Configuration()

config.section_("User")
#config.User.voGroup = 'cms'

config.section_("General")

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'S0_makePAT_76.py'

config.section_("Data")
#config.Data.totalUnits = 1000000 # use this only for MC, when you want to limit number of events to process

config.section_("Site")
config.Site.storageSite = "T2_PL_Swierk"

config.General.workArea='FSQ_Run2015C_lowPU_09102016'
config.General.requestName='FSQ_Run2015C_lowPU_09102016_data_FSQJets3'
config.Data.outputDatasetTag='FSQ_Run2015C_lowPU_09102016_data_FSQJets3'
config.Data.inputDataset='/FSQJets3/Run2015C_25ns-16Dec2015-v1/MINIAOD'
config.Data.splitting='LumiBased'
config.Data.unitsPerJob=10
config.Data.lumiMask='/afs/cern.ch/user/m/misiura/CMSSW_7_6_6/src/CommonFSQFramework/Skim/lumi/Cert_254986-255031_13TeV_PromptReco_Collisions15_LOWPU_25ns_JSON.txt'
