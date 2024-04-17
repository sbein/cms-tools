import copy

non_iso_2l_factors = {
    '2016' : {
        "Muons" : [0.73,0.14],
    },
    '2017' : {
        "Muons" : [0.577319562435,0.0685120763638],
    },
    '2018' : {
        "Muons" : [0.506097555161,0.0482066278651],
    },
    "phase1" : {
        "Muons" : [0.615,0.057],
    }
}


non_iso_2l_non_sos_factors = {
    '2016' : {
        "Muons" : [0.538,0.076],
    },
    "phase1" : {
        "Muons" : [0.528,0.039],
    }
}


non_iso_2l_factors_closure_line_fit = {
    '2016' : {
        "Muons" : [0.548381507397,0.0784842709934],
    },
    '2017' : {
        "Muons" : [0.538011014462,0.0638548734525],
    },
    '2018' : {  
        "Muons" : [0.44481164217,0.0423700934689],
    },
    'phase1' : {  
        "Muons" : [0.46783977747,0.0347372253605],
    },
}

non_iso_2l_factors_closure_line_fit_sigma_m = {
    '2016' : {
        "Muons" : [0.528906583786,0.0757227023209],
    },
    '2017' : {
        "Muons" : [0.50672185421,0.0601354942269],
    },
    '2018' : {  
        "Muons" : [0.450082242489,0.0428743577446],
    },
    'phase1' : {  
        "Muons" : [0.473201811314,0.0351371700556],
    },
}

non_iso_2l_factors_base = copy.deepcopy(non_iso_2l_factors)
non_iso_2l_factors_sigma = copy.deepcopy(non_iso_2l_factors)

# The comments here are because we don't treat 2016 as different now...
#non_iso_2l_factors_base['2016']['Muons'] = non_iso_2l_factors_closure_line_fit['2016']['Muons']
#non_iso_2l_factors_sigma['2016']['Muons'] = non_iso_2l_factors_closure_line_fit_sigma_m['2016']['Muons']

non_iso_2l_factors_sigma['2016']['Muons'] = non_iso_2l_factors_closure_line_fit['2016']['Muons']
non_iso_2l_factors_sigma['2017']['Muons'] = non_iso_2l_factors_closure_line_fit['2017']['Muons']
non_iso_2l_factors_sigma['2018']['Muons'] = non_iso_2l_factors_closure_line_fit['2018']['Muons']
non_iso_2l_factors_sigma['phase1']['Muons'] = non_iso_2l_factors_closure_line_fit['phase1']['Muons']

non_iso_1t_factors = {
    '2016' : {
        "Electrons" : [1.039,0.05],
        "Muons" : [1.11, 0.043],
    },
    '2017' : {
        "Electrons" : [1.06451618671,0.119074677517],
        "Muons" : [0.953716695309,0.0511205737877],
    },
    '2018' : {
        "Electrons" : [1.02030456066,0.102291659779],
        "Muons" : [1.11734688282,0.0491334201941],
    },
    'phase1' : {
        "Electrons" : [1.049,0.03],
        "Muons" : [1.066,0.024],
    },
}

sfs = {
    "tracks" : non_iso_1t_factors,
    "leptons" : non_iso_2l_factors
}

tautau_factors = {
    "2016" : {
        "Muons" : [1.178,0.45],
    },
    "phase1" : {
        "Muons" : [0.28,0.26],
    },
}

tautau_windows = {
    "Muons" : [40,130],
    "Electrons" : [0,160]
}

binning = {
    #Add more binning for the phase1
    "1t" : {
        "2016":{
            "Electrons" : [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1],
            "Muons" : [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,1]
        },
        "phase1":{
            "Electrons" : [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,1],
            "Muons" : [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,1]
        }
    },
    "2l" : {

        "Electrons" : [0,0.1,0.2,0.3,1],
        #new 
        "Muons" : [0,0.1,0.2,0.3,0.4,0.5,1] 
    }
}

track_mva_cut = {
    "Electrons" : 0.0,
    "Muons" : 0.0
}

###### COMMAND TO COMPARE #######
#cat tmp | tr '&&' '\n' | sort | uniq |sed 's/^ *//g' |sort

uniform_binning_number = 40

luminosities_before_topup = {
    '2016' : 35.7389543,
    '2017' : 41.14712197,
    '2018' : 58.090723828,
    "phase1" : 99.226209715
}

luminosities = {
    '2016' : 36.2,
    '2017' : 41.4,
    '2018' : 58.92,
    "phase1" : 100.32
}

luminosities_labels = {
    '2016' : 36,
    '2017' : 41,
    '2018' : 60,
    "phase1" : 101,
    "run2" : 137
}

recommended_luminosities = {
    '2016' : 36.31,
    '2017' : 41.48,
    '2018' : 59.83,
    "phase1" : 101.3,
    "run2" : 137
}


fast_sim_weights = {
    '2016' : "Weight * BranchingRatio",# * FastSimWeightPR31285To36122 #only if we want to try to run the pMSSM
    '2017' : "Weight * BranchingRatio",
    '2018' : "Weight * BranchingRatio  * hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons",
    "phase1" : "Weight * BranchingRatio * (("+ "{:.2f}".format(luminosities["2017"] * 1000) +" + "+ "{:.2f}".format(luminosities["2018"] * 1000) +" /" + "{:.2f}".format((luminosities["2017"]+luminosities["2018"]) * 1000)  + ") * hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons"
}

full_sim_weights  = {
    '2016' : "Weight * BranchingRatio * tEffhMetMhtRealXMht2016",
    '2017' : "Weight * BranchingRatio * tEffhMetMhtRealXMht2017",
    '2018' : "Weight * BranchingRatio * tEffhMetMhtRealXMht2018 * hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons",
    "phase1" : "Weight * BranchingRatio * (("+ "{:.2f}".format(luminosities["2017"] * 1000) +" * tEffhMetMhtRealXMht2017 + "+ "{:.2f}".format(luminosities["2018"] * 1000) +" * tEffhMetMhtRealXMht2018)/" + "{:.2f}".format((luminosities["2017"]+luminosities["2018"]) * 1000)  + ") * hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons"
}

data_weights = {
    '2016' : "",
    '2017' : "",
    '2018' : "hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons * ",
    "phase1" : "hemFailureVetoElectrons * hemFailureVetoJets * hemFailureVetoMuons * "
}

dilepBDTString = {
    '2016' : "dilepBDTphase1",
    '2017' : "dilepBDT",
    '2018' : "dilepBDT",
    "phase1" : "dilepBDT",
}

exTrackDilepBDTString = {
    '2016' : "exTrack_dilepBDT",
    '2017' : "exTrack_dilepBDT",
    '2018' : "exTrack_dilepBDT",
    "phase1" : "exTrack_dilepBDT",
}

exTrackSameSignDilepBDTString = {
    '2016' : "sc_exTrack_dilepBDT",
    '2017' : "sc_exTrack_dilepBDT",
    '2018' : "sc_exTrack_dilepBDT",
    "phase1" : "sc_exTrack_dilepBDT",
}

jetIsos = {
    "Electrons": "CorrJetNoMultIso10Dr0.5",
    "Muons" : "CorrJetNoMultIso10Dr0.6"
}

########## EXTRA WEIGHTS ##########

muonsClosureLineFitWeight = "muonsClosureLineFitWeight%%%"
muonsClosureLineFitSigmaMWeight = "muonsClosureLineFitSigmaMWeight%%%"

extra_filters_2l_main_prediction =  {
    '2016' : {
        "Electrons" : [],
        # we don't treat it as different anymore
        #"Muons" : [muonsClosureLineFitWeight],
        "Muons" : []
    },
    '2017' : {
        "Electrons" : [],
        "Muons" : [],
    },
    '2018' : {
        "Electrons" : [],
        "Muons" : [],
    },
    'phase1' : {
        "Electrons" : [],
        "Muons" : [],
    },
}

extra_filters_2l_sigma_prediction =  {
    '2016' : {
        "Electrons" : [],
        # we don't treat it as different anymore
        #"Muons" : [muonsClosureLineFitSigmaMWeight],
        "Muons" : [muonsClosureLineFitWeight],
    },
    '2017' : {
        "Electrons" : [],
        "Muons" : [muonsClosureLineFitWeight],
    },
    '2018' : {
        "Electrons" : [],
        "Muons" : [muonsClosureLineFitWeight],
    },
    'phase1' : {
        "Electrons" : [],
        "Muons" : [muonsClosureLineFitWeight],
    },
}

########## SELECTIONS ##########

common_preselection = "passedMhtMet6pack && passesUniversalSelection && MinDeltaPhiMhtJets > 0.4 && MHT >= 220 &&  MET >= 140 && BTagsDeepMedium == 0 && vetoElectronsPassIso == 0 && vetoMuonsPassIso == 0"

two_leptons_condition = "twoLeptons%%% == 1 && leptonFlavour%%% == \"$$$\""
two_leptons_condition_zoo_removal  = "invMass%%% < 12  && invMass%%% > 0.4 && !(invMass%%% > 3 && invMass%%% < 3.2) && !(invMass%%% > 0.75 && invMass%%% < 0.81)"
two_leptons_iso_condition = "isoCr%%% == 0"
two_leptons_iso_sb_condition = "isoCr%%% > 0"
two_leptons_same_sign = "sameSign%%% == 1"
two_leptons_opposite_sign = "sameSign%%% == 0"

### This should be for example dilepBDTCorrJetNoMultIso10Dr0.6 > 0 
two_leptons_bdt_sr = "***%%% > 0"
two_leptons_bdt_cr = "***%%% < 0"

sos_orth_condition = "(leptons%%%[1].Pt() <= 3.5 || deltaR%%% <= 0.3)"

mtautau_veto = "(nmtautau%%% < ^^^ || nmtautau%%% > @@@)"
inside_mtautau_window = "nmtautau%%% > ^^^ && nmtautau%%% < @@@"

tautau_mc = "tautau%%%"
not_tautau_mc = "!tautau%%%"

###### PRE MADE LISTS ###### 

two_leptons_full_bdt_conditions = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_condition, two_leptons_opposite_sign]
two_leptons_sr_conditions = two_leptons_full_bdt_conditions + [two_leptons_bdt_sr]
two_leptons_cr_conditions = two_leptons_full_bdt_conditions + [two_leptons_bdt_cr]

###### FINAL VERSION FOR THE SIGNALS ###### 
two_leptons_full_bdt_conditions_outside_mtautau_window = two_leptons_full_bdt_conditions + [mtautau_veto]
two_leptons_full_bdt_conditions_outside_mtautau_window_sos = two_leptons_full_bdt_conditions_outside_mtautau_window + [sos_orth_condition]

two_leptons_bdt_sr_iso_sb = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_sb_condition, two_leptons_opposite_sign, two_leptons_bdt_sr]
two_leptons_bdt_sr_iso_sb_outside_mtautau_window = two_leptons_bdt_sr_iso_sb + [mtautau_veto]

######## USED FOR DATA DRIVEN PREDICTION - ISOLATION SIDE BAND IN FULL BDT SCALE ########

two_leptons_full_bdt_iso_sb = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_sb_condition, two_leptons_opposite_sign]
two_leptons_full_bdt_iso_sb_outside_mtautau_window = two_leptons_full_bdt_iso_sb + [mtautau_veto]
two_leptons_full_bdt_iso_sb_outside_mtautau_window_sos = two_leptons_full_bdt_iso_sb_outside_mtautau_window + [sos_orth_condition]

two_leptons_sr_conditions_sos = two_leptons_sr_conditions + [sos_orth_condition]
two_leptons_cr_conditions_sos = two_leptons_cr_conditions + [sos_orth_condition]
two_leptons_cr_conditions_sos_not_tautau = two_leptons_cr_conditions_sos + [not_tautau_mc]

#### OUTSIDE MTAUTAU WINDOW #####

two_leptons_cr_conditions_outside_mtautau_window_basic = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, mtautau_veto, two_leptons_bdt_cr]
two_leptons_cr_conditions_outside_mtautau_window  = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, mtautau_veto]
# two_leptons_cr_conditions_outside_mtautau_window_sos = two_leptons_cr_conditions_outside_mtautau_window + [sos_orth_condition]
# two_leptons_cr_conditions_outside_mtautau_window_iso_sb = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_sb_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, mtautau_veto]
# two_leptons_cr_conditions_outside_mtautau_window_iso_sb_sos = two_leptons_cr_conditions_outside_mtautau_window_iso_sb + [sos_orth_condition]
# two_leptons_cr_conditions_outside_mtautau_window_same_sign = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_condition, two_leptons_same_sign, two_leptons_bdt_cr, mtautau_veto]
# two_leptons_cr_conditions_outside_mtautau_window_same_sign_sos = two_leptons_cr_conditions_outside_mtautau_window_same_sign + [sos_orth_condition]
# two_leptons_cr_conditions_outside_mtautau_window_same_sign_iso_sb = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_sb_condition, two_leptons_same_sign, two_leptons_bdt_cr, mtautau_veto]
# two_leptons_cr_conditions_outside_mtautau_window_same_sign_iso_sb_sos = two_leptons_cr_conditions_outside_mtautau_window_same_sign_iso_sb + [sos_orth_condition]

###### USED FOR MC TAU TAU TRANSFER FACTOR - TAU TAU - INSIDE TAU-TAU WINDOW #########
two_leptons_bdt_cr_tautau_inside_mtautau_window = [common_preselection, two_leptons_condition, two_leptons_iso_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, inside_mtautau_window, tautau_mc]
two_leptons_bdt_cr_tautau_inside_mtautau_window_sos = two_leptons_bdt_cr_tautau_inside_mtautau_window + [sos_orth_condition]
###### USED FOR MC TAU TAU PREDICTION - TAU TAU - OUTSIDE TAU-TAU WINDOW #########
two_leptons_full_bdt_tautau_outside_mtautau_window_prediction = [common_preselection, two_leptons_condition, two_leptons_iso_condition, two_leptons_condition_zoo_removal, two_leptons_opposite_sign, tautau_mc, mtautau_veto] 
two_leptons_full_bdt_tautau_outside_mtautau_window_prediction_sos = two_leptons_full_bdt_tautau_outside_mtautau_window_prediction + [sos_orth_condition]

###### MC - NOT TAU TAU - INSIDE/OUTSIDE TAU-TAU WINDOW #########

two_leptons_sr_conditions_not_tautau = two_leptons_sr_conditions + [not_tautau_mc]
two_leptons_sr_conditions_sos_not_tautau = two_leptons_sr_conditions_not_tautau + [sos_orth_condition]

###### INSIDE ######
two_leptons_bdt_cr_not_tautau_inside_mtautau_window  = [common_preselection, two_leptons_condition, two_leptons_iso_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, inside_mtautau_window, not_tautau_mc]
two_leptons_bdt_cr_not_tautau_inside_mtautau_window_sos = two_leptons_bdt_cr_not_tautau_inside_mtautau_window + [sos_orth_condition]
two_leptons_bdt_cr_not_tautau_inside_mtautau_window_iso_sb = [common_preselection, two_leptons_condition, two_leptons_iso_sb_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, inside_mtautau_window, not_tautau_mc]
two_leptons_bdt_cr_not_tautau_inside_mtautau_window_iso_sb_sos = two_leptons_bdt_cr_not_tautau_inside_mtautau_window_iso_sb + [sos_orth_condition]
###### INSIDE INCLUSIVE #####
two_leptons_bdt_cr_inside_mtautau_window  = [common_preselection, two_leptons_condition, two_leptons_iso_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, inside_mtautau_window]
two_leptons_bdt_cr_inside_mtautau_window_sos = two_leptons_bdt_cr_inside_mtautau_window + [sos_orth_condition]
two_leptons_bdt_cr_inside_mtautau_window_iso_sb = [common_preselection, two_leptons_condition, two_leptons_iso_sb_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, inside_mtautau_window]
two_leptons_bdt_cr_inside_mtautau_window_iso_sb_sos = two_leptons_bdt_cr_inside_mtautau_window_iso_sb + [sos_orth_condition]
###### OUTSIDE ######
two_leptons_bdt_cr_not_tautau_outside_mtautau_window = two_leptons_cr_conditions_outside_mtautau_window + [not_tautau_mc]
two_leptons_bdt_cr_not_tautau_outside_mtautau_window_sos = two_leptons_bdt_cr_not_tautau_outside_mtautau_window + [sos_orth_condition]
two_leptons_bdt_cr_not_tautau_outside_mtautau_window_iso_sb = [common_preselection, two_leptons_condition, two_leptons_condition_zoo_removal, two_leptons_iso_sb_condition, two_leptons_opposite_sign, two_leptons_bdt_cr, mtautau_veto, not_tautau_mc]
two_leptons_bdt_cr_not_tautau_outside_mtautau_window_iso_sb_sos = two_leptons_bdt_cr_not_tautau_outside_mtautau_window_iso_sb + [sos_orth_condition]

######## EXCLUSIVE TRACKS ##########

ex_track_cond = "exclusiveTrack%%% == 1 && trackBDT%%% > 0 && exTrack_invMass%%% < 12  && exclusiveTrackLeptonFlavour%%% == \"$$$\""
sc_ex_track_cond = "sc_exclusiveTrack%%% == 1 && sc_trackBDT%%% > 0 && sc_exTrack_invMass%%% < 12 && sc_exclusiveTrackLeptonFlavour%%% == \"$$$\""

ex_track_electrons_filter = "exTrack_deltaR%%% > 0.05"
sc_ex_track_electrons_filter = "sc_exTrack_deltaR%%% > 0.05"

ex_track_cr = "exTrack_dilepBDT%%% < 0"
sc_ex_track_cr = "sc_exTrack_dilepBDT%%% < 0"

ex_track_cr_selections = [common_preselection, ex_track_cond, ex_track_cr]
ex_track_cr_electrons_selections = ex_track_cr_selections + [ex_track_electrons_filter]

sc_ex_track_cr_selections = [common_preselection, sc_ex_track_cond, sc_ex_track_cr]
sc_ex_track_cr_electrons_selections = sc_ex_track_cr_selections + [sc_ex_track_electrons_filter]


#exclusive_track_category =  "exclusiveTrack%%% == 1 && exTrack_invMass%%% < 12 && exclusiveTrackLeptonFlavour%%% ==\"$$$\" && trackBDT%%% > 0"
#exclusive_track_category_sr = "exTrack_dilepBDT%%% > 0"
#exclusive_track_category_cr = "exTrack_dilepBDT%%% < 0"

#electrons_extra_exclusive_track_category = "exclusive_track_category%%% > 0.05"

#sc_exclusive_track_category = "sc_exclusiveTrack%%% == 1 && sc_exTrack_invMass%%% < 12 && sc_exclusiveTrackLeptonFlavour%%% == \"$$$\" && sc_trackBDT%%% > 0 &&"
#sc_exclusive_track_category_sr = "sc_exTrack_dilepBDT%%% > 0"
#sc_exclusive_track_category_cr = "sc_exTrack_dilepBDT%%% < 0"

#sc_electrons_extra_exclusive_track_category = "sc_exTrack_deltaR%%% > 0.05"

####### FOR CREATING PREDICTIONS AND SIGNALS ####### 

ex_track_full_range_selections = [common_preselection, ex_track_cond]
ex_track_full_range_selections_electrons = ex_track_full_range_selections + [ex_track_electrons_filter]

sc_ex_track_full_range_selections = [common_preselection, sc_ex_track_cond]
sc_ex_track_full_range_selections_electrons = sc_ex_track_full_range_selections + [sc_ex_track_electrons_filter]


def injectValues(toReplace, year, flavour):    
    return toReplace.replace("%%%", jetIsos[flavour]).replace("^^^", str(tautau_windows[flavour][0])).replace("@@@", str(tautau_windows[flavour][1])).replace("$$$", flavour).replace("***", dilepBDTString[year])

def getFastSimString(year, flavour, selections): ##will add a 4th argument: extraFilters = []
    return injectValues("{:.2f}".format(luminosities[year] * 1000) + " * " + fast_sim_weights[year] + " * (" + andStringSelections(selections) + ")", year, flavour)

def getFullSimString(year, flavour, selections):
    return injectValues("{:.2f}".format(luminosities[year] * 1000) + " * " +full_sim_weights[year] + " * (" + andStringSelections(selections) + ")", year, flavour)

def getDataString(year, flavour, selections, extraFilters = []):
    return injectValues(" * ".join(extraFilters) + (" * " if len(extraFilters) > 0 else "") +  data_weights[year] + "(" + andStringSelections(selections) + ")", year, flavour)

def andStringSelections(selections):
    return " && ".join(selections)
