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

