import FWCore.ParameterSet.Config as cms

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
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/00000/8EA8FE89-254F-E811-835E-0090FAA58BF4.root',
    )
)

OUTFILENAME = 'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_FWLJMET_MC.root'
# TFileService
process.TFileService = cms.Service("TFileService", fileName = cms.string(OUTFILENAME))



process.ljmet = cms.EDAnalyzer(
	'LJMet',

	debug         = cms.bool(True),
	selector      = cms.string('MultiLepSelector'),
	include_calcs = cms.vstring(
			'MultiLepCalc',
	),
	exclude_calcs = cms.vstring(
			'TestCalc',
			'DummyCalc',
	),

	MultiLepSelector = cms.PSet( # name has to match the name as registered in BeginJob of  EventSelector.cc

            debug  = cms.bool(True),

            isMc  = cms.bool(True),
                        
			# Trigger cuts
            HLTcollection       = cms.InputTag("TriggerResults","","HLT"),
			trigger_cut  = cms.bool(True),
			dump_trigger = cms.bool(True),
			mctrigger_path_el = cms.vstring(        
				'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v',  #exists in 2017    
				'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', #exists in 2017        

				'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',   #exists in 2017 
				'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', #exists in 2017 
				'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v', #exists in 2017  
				'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',  #exists in 2017

				#for trig efficiency
				'HLT_Ele27_WPTight_Gsf_v',
				'HLT_Ele35_WPTight_Gsf_v',
				),
			mctrigger_path_mu = cms.vstring(
				'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',   #exists in 2017 
				'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', #exists in 2017 
				'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v', #exists in 2017  
				'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',  #exists in 2017

				'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v',    #exists in 2017  (PreScaled!)        
				'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v',  #exists in 2017 (PreScaled!)        
				'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v',                      
				'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v',           
				'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v',        

				#for trig efficiency
				'HLT_IsoMu24_v',
				'HLT_IsoTkMu24_v',
				'HLT_IsoMu27_v',
				),
			trigger_path_el = cms.vstring(''),
			trigger_path_mu = cms.vstring(''),
			
			# PV cuts
			pv_cut         = cms.bool(True),
			pvSelector = cms.PSet( # taken from https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/PhysicsTools/SelectorUtils/python/pvSelector_cfi.py
				NPV     = cms.int32(1),
				pvSrc   = cms.InputTag('offlineSlimmedPrimaryVertices'),
				minNdof = cms.double(4.0),
				maxZ    = cms.double(24.0),
				maxRho  = cms.double(2.0)
				),
				
			# MET filter - https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2 
			metfilters      = cms.bool(True),
			flag_tag        = cms.InputTag('TriggerResults::PAT'),
			METfilter_extra = cms.InputTag("ecalBadCalibReducedMINIAODFilter"),
			
			#MET cuts
			met_cuts    = cms.bool(False),
			min_met     = cms.double(20.0),
			max_met     = cms.double(99999999999.0),
			met_collection           = cms.InputTag('slimmedMETs'),


            PFparticlesCollection  = cms.InputTag("packedPFCandidates"),
            rhoInputTag            = cms.InputTag("fixedGridRhoFastjetCentralNeutral",""),
            
            #Muon
            muonsCollection        = cms.InputTag("slimmedMuons"),
			muon_cuts                = cms.bool(True),
			min_muon                 = cms.int32(0),
			muon_minpt               = cms.double(20.0),
			muon_maxeta              = cms.double(2.4),
			muon_useMiniIso          = cms.bool(True),
			muon_miniIso             = cms.double(0.2),
			loose_muon_miniIso       = cms.double(0.4),
			loose_muon_minpt         = cms.double(20.0),
			loose_muon_maxeta        = cms.double(2.4),
			muon_dxy                 = cms.double(0.2),
			muon_dz                  = cms.double(0.5),
			loose_muon_dxy           = cms.double(999999.),
			loose_muon_dz            = cms.double(999999.),

			# Muon -- Unused parameters but could be use again
			muon_relIso              = cms.double(0.2),
			loose_muon_relIso        = cms.double(0.4),


            electronsCollection    = cms.InputTag("slimmedElectrons"),



            minLeptons = cms.int32(3),

            min_muPt   = cms.double(20.),
            max_muEta  = cms.double(2.4),
            min_elPt   = cms.double(20.),
            max_elEta  = cms.double(2.4),

            ),
            
			
	MultiLepCalc = cms.PSet( # name has to match the calculator name as registered in Calc.cc

	    debug  = cms.bool(True),
            electronsCollection = cms.InputTag("slimmedElectrons"),

	),


)



# Configure a path and endpath to run the producer and output modules
process.p = cms.Path(
	process.ljmet
)