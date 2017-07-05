anaVersion="FSQ_Run2015C_lowPU_20161108"
anaType="FSQ_Run2015C_lowPU"

cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"

sam = {}

sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]={}
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["crabJobs"]=10
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["GT"]='76X_mcRun2_asymptotic_v12'
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["name"]='QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp'
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["isData"]=False
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["numEvents"]=997904
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["json"]=''
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["lumiMinBias"]=0.0
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["XS"]=1545000000
sam["QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp"]["DS"]='/QCD_Pt-10to35_TuneCUETHS1_13TeV-herwigpp/RunIIFall15MiniAODv2-PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'

sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]={}
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["crabJobs"]=10
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["GT"]='76X_mcRun2_asymptotic_v12'
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["name"]='QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp'
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["isData"]=False
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["numEvents"]=976276
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["json"]=''
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["lumiMinBias"]=0.0
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["XS"]=18240000
sam["QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp"]["DS"]='/QCD_Pt-35toInf_TuneCUETHS1_13TeV-herwigpp/RunIIFall15MiniAODv2-PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'

sam["data_FSQJets3"]={}
sam["data_FSQJets3"]["crabJobs"]=0
sam["data_FSQJets3"]["GT"]='76X_dataRun2_v15'
sam["data_FSQJets3"]["name"]='data_FSQJets3'
sam["data_FSQJets3"]["isData"]=True
sam["data_FSQJets3"]["numEvents"]=-1
sam["data_FSQJets3"]["json"]='CommonFSQFramework/Skim/lumi/Cert_254986-255031_13TeV_PromptReco_Collisions15_LOWPU_25ns_JSON.txt'
sam["data_FSQJets3"]["lumiMinBias"]=-1
sam["data_FSQJets3"]["XS"]=-1
sam["data_FSQJets3"]["DS"]='/FSQJets3/Run2015C_25ns-16Dec2015-v1/MINIAOD'


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
