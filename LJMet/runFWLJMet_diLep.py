import FWCore.ParameterSet.Config as cms
import os


relBase = os.environ['CMSSW_BASE']

process = cms.Process("LJMET")

## MessageLogger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 20

## Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

## Maximal Number of Events
MAXEVENTS = 100
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(MAXEVENTS) )

## Source / Input
isMC=True
#isMC=False
if(isMC): INFILE='root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/00000/8EA8FE89-254F-E811-835E-0090FAA58BF4.root'
else: INFILE='root://cmsxrootd.fnal.gov//store/data/Run2017F/DoubleEG/MINIAOD/09May2018-v1/10000/444E03EB-B75F-E811-AFBA-F01FAFD8F16A.root'

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        INFILE,
    )
)

if(isMC):
        OUTFILENAME = 'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8'
        POSTFIX = 'MC'
else:
        OUTFILENAME = 'DoubleEG_Run2017F'
        POSTFIX = 'DATA'
# TFileService
process.TFileService = cms.Service("TFileService", fileName = cms.string(OUTFILENAME+'_FWLJMET_dilep'+POSTFIX+'.root'))


# Output Module Configuration (expects a path 'p')
# process.out = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string(OUTFILENAME+'_postReco_MC.root'),
#                                #SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
#                                #outputCommands = cms.untracked.vstring('keep *')
#                                )


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v17', '')
if isMC == False: process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_v11')
print 'Using global tag', process.GlobalTag.globaltag



## Produce new slimmedElectrons with V2 IDs
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True,
                       era='2017-Nov17ReReco')


## Produce modified MET with the ECAL noise fix
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

runMetCorAndUncFromMiniAOD(
    process,
    isData = not isMC,
    fixEE2017 = True,
    fixEE2017Params = {'userawPt': True, 'ptThreshold':50.0, 'minEtaThreshold':2.65, 'maxEtaThreshold': 3.139},
    postfix = "ModifiedMET"
    )



#For MET filter
if(isMC): MET_filt_flag_tag        = 'TriggerResults::PAT'
else:     MET_filt_flag_tag        = 'TriggerResults::RECO'

#For Jet corrections
doNewJEC                 = True
JECup                    = False
JECdown                  = False
JERup                    = False
JERdown                  = False
doAllJetSyst             = False #this determines whether to save JER/JER up/down in one job. Default is currently false. Mar 19,2019.
JEC_txtfile              = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.txt'
JERSF_txtfile            = relBase+'/src/FWLJMET/LJMet/data/Fall17V3/Fall17_V3_MC_SF_AK4PFchs.txt'
JER_txtfile              = relBase+'/src/FWLJMET/LJMet/data/Fall17V3/Fall17_V3_MC_PtResolution_AK4PFchs.txt'
JERAK8_txtfile           = relBase+'/src/FWLJMET/LJMet/data/Fall17V3/Fall17_V3_MC_PtResolution_AK8PFPuppi.txt'
MCL1JetPar               = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.txt'
MCL2JetPar               = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.txt'
MCL3JetPar               = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L3Absolute_AK4PFchs.txt'
MCL1JetParAK8            = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L1FastJet_AK8PFPuppi.txt'
MCL2JetParAK8            = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L2Relative_AK8PFPuppi.txt'
MCL3JetParAK8            = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017_V32_MC_L3Absolute_AK8PFPuppi.txt'
DataL1JetPar             = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L1FastJet_AK4PFchs.txt'
DataL2JetPar             = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2Relative_AK4PFchs.txt'
DataL3JetPar             = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L3Absolute_AK4PFchs.txt'
DataResJetPar            = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2L3Residual_AK4PFchs.txt'
DataL1JetParAK8          = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L1FastJet_AK8PFPuppi.txt'
DataL2JetParAK8          = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2Relative_AK8PFPuppi.txt'
DataL3JetParAK8          = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L3Absolute_AK8PFPuppi.txt'
DataResJetParAK8         = relBase+'/src/FWLJMET/LJMet/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2L3Residual_AK8PFPuppi.txt'


DileptonSelector_cfg = cms.PSet(

            debug  = cms.bool(True),

            isMc  = cms.bool(isMC),

            # Trigger cuts
            trigger_cut  = cms.bool(True),
            HLTcollection= cms.InputTag("TriggerResults","","HLT"),
            dump_trigger = cms.bool(False),
            trigger_path_ee          = cms.vstring(
                'HLT_DoubleEle33_CaloIdL_MW_v',
                'HLT_DoubleEle27_CaloIdL_MW_v',
                'HLT_DoubleEle25_CaloIdL_MW_v',
                'HLT_Ele27_Ele37_CaloIdL_MW_v',

                'HLT_DoubleEle24_eta2p1_WPTight_Gsf_v',
                'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v',
                'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v',
                'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
                'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v',

                ),

            trigger_path_em          = cms.vstring(
                'HLT_Mu37_Ele27_CaloIdL_MW_v',
                'HLT_Mu27_Ele37_CaloIdL_MW_v',

                'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v',
                'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
                'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_v',
                'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',
                'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
                'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
                'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',
                'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',
                ),

            trigger_path_mm          = cms.vstring(
                'HLT_Mu37_TkMu27_v',
                'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v',
                'HLT_DoubleMu8_Mass8_PFHT350_v',
                'HLT_DoubleMu4_Mass8_DZ_PFHT350_v',
                ),

            # PV cuts
            pv_cut     = cms.bool(True),
            pvSelector = cms.PSet( # taken from https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/PhysicsTools/SelectorUtils/python/pvSelector_cfi.py
                        NPV     = cms.int32(1),
                        pvSrc   = cms.InputTag('offlineSlimmedPrimaryVertices'),
                        minNdof = cms.double(4.0),
                        maxZ    = cms.double(24.0),
                        maxRho  = cms.double(2.0)
                        ),

            # MET filter - https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
            metfilters      = cms.bool(True),
            flag_tag        = cms.InputTag(MET_filt_flag_tag),
            METfilter_extra = cms.InputTag("ecalBadCalibReducedMINIAODFilter"),

            # MET cuts
            # met_cuts       = cms.bool(True),
            # min_met        = cms.double(20.0),
            # max_met        = cms.double(99999999999.0),
            # met_collection = cms.InputTag('slimmedMETs'),
            # rhoJetsInputTag = cms.InputTag("fixedGridRhoFastjetAll"), #for jetmetcorrection

            # PFparticlesCollection  = cms.InputTag("packedPFCandidates"),
            # rhoJetsNCInputTag            = cms.InputTag("fixedGridRhoFastjetCentralNeutral",""),

            # #Muon
            # muon_cuts                = cms.bool(True),
            # muonsCollection          = cms.InputTag("slimmedMuons"),
            # min_muon                 = cms.int32(0), #not implemented in src code
            # muon_minpt               = cms.double(20.0),
            # muon_maxeta              = cms.double(2.4),
            # muon_useMiniIso          = cms.bool(True),
            # loose_muon_minpt         = cms.double(20.0),
            # loose_muon_maxeta        = cms.double(2.4),
            # muon_dxy                 = cms.double(0.2),
            # muon_dz                  = cms.double(0.5),
            # loose_muon_dxy           = cms.double(999999.),
            # loose_muon_dz            = cms.double(999999.),

            # # Muon -- Unused parameters but could be use again
            # muon_relIso              = cms.double(0.2),
            # loose_muon_relIso        = cms.double(0.4),

            # # Electon
            # electron_cuts            = cms.bool(True),
            # electronsCollection      = cms.InputTag("slimmedElectrons"), #slimmedElectrons::LJMET" #for Egamma ID V2
            # min_electron             = cms.int32(0), #not implemented in src code
            # electron_minpt           = cms.double(20.0),
            # electron_maxeta          = cms.double(2.4),
            # electron_useMiniIso      = cms.bool(True),
            # electron_miniIso         = cms.double(0.1),
            # loose_electron_miniIso   = cms.double(0.4),
            # loose_electron_minpt     = cms.double(20.0),
            # loose_electron_maxeta    = cms.double(2.4),
            # UseElMVA                 = cms.bool(True),
            # UseElIDV1                = cms.bool(True), #False means using ElIDV2

            # #nLeptons
            # minLooseLeptons_cut = cms.bool(True), #inclusive Loose.
            # minLooseLeptons     = cms.int32(3),
            # maxLooseLeptons_cut = cms.bool(False),
            # maxLooseLeptons     = cms.int32(9999),
            # minLeptons_cut      = cms.bool(False),
            # minLeptons          = cms.int32(3),
            # maxLeptons_cut      = cms.bool(False),
            # maxLeptons          = cms.int32(9999),

            # # Jets
            # jet_collection           = cms.InputTag('slimmedJets'),
            # AK8jet_collection        = cms.InputTag('slimmedJetsAK8'),
            # JECup                    = cms.bool(JECup),
            # JECdown                  = cms.bool(JECdown),
            # JERup                    = cms.bool(JERup),
            # JERdown                  = cms.bool(JERdown),
            # doLepJetCleaning         = cms.bool(True),
            # CleanLooseLeptons        = cms.bool(True),
            # LepJetDR                 = cms.double(0.4),
            # LepJetDRAK8              = cms.double(0.8),
            # jet_cuts                 = cms.bool(True),
            # jet_minpt                = cms.double(30.0),
            # jet_maxeta               = cms.double(2.5),
            # jet_minpt_AK8            = cms.double(200.0),
            # jet_maxeta_AK8           = cms.double(2.4),
            # min_jet                  = cms.int32(1),
            # max_jet                  = cms.int32(9999),
            # leading_jet_pt           = cms.double(30.0),
            # # Jet corrections are read from txt files
            # doNewJEC                 = cms.bool(doNewJEC),
            # doAllJetSyst             = cms.bool(doAllJetSyst),
            # JEC_txtfile              = cms.string(JEC_txtfile),
            # JERSF_txtfile            = cms.string(JERSF_txtfile),
            # JER_txtfile              = cms.string(JER_txtfile),
            # JERAK8_txtfile           = cms.string(JERAK8_txtfile),
            # MCL1JetPar               = cms.string(MCL1JetPar),
            # MCL2JetPar               = cms.string(MCL2JetPar),
            # MCL3JetPar               = cms.string(MCL3JetPar),
            # MCL1JetParAK8            = cms.string(MCL1JetParAK8),
            # MCL2JetParAK8            = cms.string(MCL2JetParAK8),
            # MCL3JetParAK8            = cms.string(MCL3JetParAK8),
            # DataL1JetPar             = cms.string(DataL1JetPar),
            # DataL2JetPar             = cms.string(DataL2JetPar),
            # DataL3JetPar             = cms.string(DataL3JetPar),
            # DataResJetPar            = cms.string(DataResJetPar),
            # DataL1JetParAK8          = cms.string(DataL1JetParAK8),
            # DataL2JetParAK8          = cms.string(DataL2JetParAK8),
            # DataL3JetParAK8          = cms.string(DataL3JetParAK8),
            # DataResJetParAK8         = cms.string(DataResJetParAK8),


            # #Btag
            # btag_cuts                = cms.bool(False), #not implemented
            # btagOP                   = cms.string('MEDIUM'),
            # bdisc_min                = cms.double(0.4941), # THIS HAS TO MATCH btagOP !
            # applyBtagSF              = cms.bool(True), #This is implemented by BTagSFUtil.cc
            # DeepCSVfile              = cms.string(relBase+'/src/FWLJMET/LJMet/data/DeepCSV_94XSF_V3_B_F.csv'),
            # DeepCSVSubjetfile        = cms.string(relBase+'/src/FWLJMET/LJMet/data/subjet_DeepCSV_94XSF_V3_B_F.csv'),
            # BTagUncertUp             = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            # BTagUncertDown           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            # MistagUncertUp           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            # MistagUncertDown          = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.

            )

MultiLepCalc_cfg = cms.PSet(

            debug                  = cms.bool(True),
            isMc                   = cms.bool(isMC),
            saveLooseLeps          = cms.bool(True),
            keepFullMChistory      = cms.bool(isMC),

            rhoJetsNCInputTag      = cms.InputTag("fixedGridRhoFastjetCentralNeutral",""), #this is for muon
            genParticlesCollection = cms.InputTag("prunedGenParticles"),
            PFparticlesCollection  = cms.InputTag("packedPFCandidates"),

            rhoJetsInputTag            = cms.InputTag("fixedGridRhoFastjetAll"), #this is for electron. Why is it different compared to muon?
            UseElMVA                 = cms.bool(True),
            UseElIDV1                = cms.bool(True), #False means using ElIDV2.

            # Jet corrections needs to be passed here again if Calc uses jet correction
            doNewJEC                 = cms.bool(doNewJEC),
            JECup                    = cms.bool(JECup),
            JECdown                  = cms.bool(JECdown),
            JERup                    = cms.bool(JERup),
            JERdown                  = cms.bool(JERdown),
            doAllJetSyst             = cms.bool(doAllJetSyst),
            JEC_txtfile              = cms.string(JEC_txtfile),
            JERSF_txtfile            = cms.string(JERSF_txtfile),
            JER_txtfile              = cms.string(JER_txtfile),
            JERAK8_txtfile           = cms.string(JERAK8_txtfile),
            MCL1JetPar               = cms.string(MCL1JetPar),
            MCL2JetPar               = cms.string(MCL2JetPar),
            MCL3JetPar               = cms.string(MCL3JetPar),
            MCL1JetParAK8            = cms.string(MCL1JetParAK8),
            MCL2JetParAK8            = cms.string(MCL2JetParAK8),
            MCL3JetParAK8            = cms.string(MCL3JetParAK8),
            DataL1JetPar             = cms.string(DataL1JetPar),
            DataL2JetPar             = cms.string(DataL2JetPar),
            DataL3JetPar             = cms.string(DataL3JetPar),
            DataResJetPar            = cms.string(DataResJetPar),
            DataL1JetParAK8          = cms.string(DataL1JetParAK8),
            DataL2JetParAK8          = cms.string(DataL2JetParAK8),
            DataL3JetParAK8          = cms.string(DataL3JetParAK8),
            DataResJetParAK8         = cms.string(DataResJetParAK8),

            #For accessing METnoHF, and METmod
            metnohf_collection = cms.InputTag('slimmedMETsNoHF'),
            metmod_collection = cms.InputTag('slimmedMETsModifiedMET'),

            #Gen stuff
            saveGenHT          = cms.bool(False),
            genJetsCollection  = cms.InputTag("slimmedGenJets"),
            OverrideLHEWeights = cms.bool(True),
            basePDFname        = cms.string('NNPDF31_nnlo_as_0118_nf_4'),
            newPDFname         = cms.string('NNPDF31_lo_as_0118'),
            keepPDGID          = cms.vuint32(1, 2, 3, 4, 5, 6, 21, 11, 12, 13, 14, 15, 16, 24),
            keepMomPDGID       = cms.vuint32(6, 24),
            keepPDGIDForce     = cms.vuint32(6,6),
            keepStatusForce    = cms.vuint32(62,22),
            cleanGenJets       = cms.bool(True),

            #Btagging - Btag info needs to be passed here again if Calc uses Btagging.
            btagOP                   = cms.string('MEDIUM'),
            bdisc_min                = cms.double(0.4941), # THIS HAS TO MATCH btagOP !
            applyBtagSF              = cms.bool(True), #This is implemented by BTagSFUtil.cc
            DeepCSVfile              = cms.string(relBase+'/src/FWLJMET/LJMet/data/DeepCSV_94XSF_V3_B_F.csv'),
            DeepCSVSubjetfile        = cms.string(relBase+'/src/FWLJMET/LJMet/data/subjet_DeepCSV_94XSF_V3_B_F.csv'),
            BTagUncertUp             = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            BTagUncertDown           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            MistagUncertUp           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            MistagUncertDown          = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.

            )

TpTpCalc_cfg = cms.PSet(

    genParticlesCollection = cms.InputTag("prunedGenParticles"),

        )

JetSubCalc_cfg = cms.PSet(

            debug        = cms.bool(False),
            isMc         = cms.bool(isMC),

            genParticles       = cms.InputTag("prunedGenParticles"),

            kappa              = cms.double(0.5), #for Jet Charge calculation
            killHF             = cms.bool(False),
            puppiCorrPath      = cms.string(relBase+'/src/FWLJMET/LJMet/data/PuppiSoftdropMassCorr/weights/puppiCorr.root'),

            rhoJetsInputTag          = cms.InputTag("fixedGridRhoFastjetAll"), #this is for electron. Why is it different compared to muon?

            # Jet recorrections needs to be passed here again if Calc uses jet correction
            doNewJEC                 = cms.bool(doNewJEC),
            JECup                    = cms.bool(JECup),
            JECdown                  = cms.bool(JECdown),
            JERup                    = cms.bool(JERup),
            JERdown                  = cms.bool(JERdown),
            doAllJetSyst             = cms.bool(doAllJetSyst),
            JEC_txtfile              = cms.string(JEC_txtfile),
            JERSF_txtfile            = cms.string(JERSF_txtfile),
            JER_txtfile              = cms.string(JER_txtfile),
            JERAK8_txtfile           = cms.string(JERAK8_txtfile),
            MCL1JetPar               = cms.string(MCL1JetPar),
            MCL2JetPar               = cms.string(MCL2JetPar),
            MCL3JetPar               = cms.string(MCL3JetPar),
            MCL1JetParAK8            = cms.string(MCL1JetParAK8),
            MCL2JetParAK8            = cms.string(MCL2JetParAK8),
            MCL3JetParAK8            = cms.string(MCL3JetParAK8),
            DataL1JetPar             = cms.string(DataL1JetPar),
            DataL2JetPar             = cms.string(DataL2JetPar),
            DataL3JetPar             = cms.string(DataL3JetPar),
            DataResJetPar            = cms.string(DataResJetPar),
            DataL1JetParAK8          = cms.string(DataL1JetParAK8),
            DataL2JetParAK8          = cms.string(DataL2JetParAK8),
            DataL3JetParAK8          = cms.string(DataL3JetParAK8),
            DataResJetParAK8         = cms.string(DataResJetParAK8),

            #Btagging - Btag info needs to be passed here again if Calc uses Btagging.
            btagOP                   = cms.string('MEDIUM'),
            bdisc_min                = cms.double(0.4941), # THIS HAS TO MATCH btagOP !
            applyBtagSF              = cms.bool(True), #This is implemented by BTagSFUtil.cc
            DeepCSVfile              = cms.string(relBase+'/src/FWLJMET/LJMet/data/DeepCSV_94XSF_V3_B_F.csv'),
            DeepCSVSubjetfile        = cms.string(relBase+'/src/FWLJMET/LJMet/data/subjet_DeepCSV_94XSF_V3_B_F.csv'),
            BTagUncertUp             = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            BTagUncertDown           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            MistagUncertUp           = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.
            MistagUncertDown          = cms.bool(False), # no longer needed, but can still be utilized. Keep false as default.

    )

process.ljmet = cms.EDAnalyzer(
        'LJMet',

        debug         = cms.bool(False),
        verbosity     = cms.int32(1),
        selector      = cms.string('DileptonSelector'),
        include_calcs = cms.vstring(
                        # 'DiLepCalc',
                        'TpTpCalc',
                        'CommonCalc',
                        # 'JetSubCalc',
        ),
        exclude_calcs = cms.vstring(
                        'TestCalc',
                        'DummyCalc',
        ),

        # name has to match the name as registered in BeginJob of  EventSelector.cc
        DileptonSelector = cms.PSet(DileptonSelector_cfg),

        # Calc cfg name has to match the name as registered in Calc.cc
        # DiLepCalc    = cms.PSet(DiLepCalc_cfg),
        TpTpCalc     = cms.PSet(TpTpCalc_cfg),
        CommonCalc   = cms.PSet(),
        # JetSubCalc   = cms.PSet(JetSubCalc_cfg),

)



# Configure a path and endpath to run the producer and output modules
process.p = cms.Path(
   process.fullPatMetSequenceModifiedMET *
#    process.egammaPostRecoSeq *
   process.ljmet
)

# process.ep = cms.EndPath(process.out)
