anaVersion="FSQ_Run2015C_lowPU_08102016"
anaType="FSQ_Run2015C_lowPU"

cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"

sam = {}

sam["data_FSQJets3"]={}
sam["data_FSQJets3"]["crabJobs"]=0
sam["data_FSQJets3"]["GT"]='76X_dataRun2_v15'
sam["data_FSQJets3"]["name"]='data_FSQJets3'
sam["data_FSQJets3"]["isData"]=True
sam["data_FSQJets3"]["numEvents"]=-1
sam["data_FSQJets3"]["json"]='CommonFSQFramework/Skim/lumi/Cert_254986-255031_13TeV_PromptReco_Collisions15_LOWPU_25ns_JSON.txt'
sam["data_FSQJets3"]["lumiMinBias"]=-1
sam["data_FSQJets3"]["XS"]=-1
sam["data_FSQJets3"]["DS"]='/FSQJets3/Run2015C_25ns-16Dec2015-v1/AOD'

sam["data_FSQJets3"]["pathSE"]=''
sam["data_FSQJets3"]["pathTrees"]='/XXXTMFTTree//CMSSW_7_6_6/src/CommonFSQFramework/Skim/config/Jets//'
sam["data_FSQJets3"]["pathPAT"]='/XXXTMFPAT//CMSSW_7_6_6/src/CommonFSQFramework/Skim/config/Jets//'

def fixLocalPaths(sam):
        import os,imp
        if "SmallXAnaDefFile" not in os.environ:
            print "Please set SmallXAnaDefFile environment variable:"
            print "export SmallXAnaDefFile=FullPathToFile"
            raise Exception("Whooops! SmallXAnaDefFile env var not defined")

        anaDefFile = os.environ["SmallXAnaDefFile"]
        mod_dir, filename = os.path.split(anaDefFile)
        mod, ext = os.path.splitext(filename)
        f, filename, desc = imp.find_module(mod, [mod_dir])
        mod = imp.load_module(mod, f, filename, desc)

        localBasePathPAT = mod.PATbasePATH
        localBasePathTrees = mod.TTreeBasePATH

        for s in sam:
            if "pathPAT" in sam[s]:
                sam[s]["pathPAT"] = sam[s]["pathPAT"].replace("XXXTMFPAT", localBasePathPAT)
            if "pathTrees" in sam[s]:
                sam[s]["pathTrees"] = sam[s]["pathTrees"].replace("XXXTMFTTree", localBasePathTrees)
            #print sam[s]["pathPAT"]
            #print sam[s]["pathTrees"]
        return sam
sam = fixLocalPaths(sam)