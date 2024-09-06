### Script provides functionality for adding new columns
### Based on system-quality, we tried multiple grouping schemes. 
### While all of those are implemented here, they are all switched off. 
### Except the one that was finally chosen - Ranks+Family crosstype. 
import sys
import pandas as pd
import numpy as np
system_name = sys.argv[1]
seq_type = sys.argv[2]


Stops = ["P", "T", "K", "B", "D", "G"]
Affricates = ["CH", "JH"]
Fricatives = ["TH", "F", "S", "SH", "HH", "DH", "V", "Z", "ZH"]

Voiced = ["B", "D", "G", "JH", "DH", "V", "Z", "ZH"]
Voiceless = ["P", "T", "K", "CH", "TH", "F", "S", "SH", "HH"]

Bilabial = ["P", "B"]
Dental = ["TH", "DH"]
Labiodental = ["F", "V"] 
Alveolar = ["T", "D", "S", "Z"]
Postalveolar = ["SH", "ZH", "CH", "JH"]
Velar = ["K", "G"]
Glottal = ["HH"]

Sibilants = ["S", "SH", "Z", "ZH"]
Non_Sibilants = ["TH", "F", "HH", "DH", "V"] 

Anterior = ["P", "T", "B", "D", "TH", "F", "S", "DH", "V", "Z"]
Posterior = ["K", "G", "CH", "JH", "SH", "ZH", "HH"]

############ System Identifiers ############
#baseline#
Natural = ["A"]
Good_Systems = ["M", "K", "I", "L", "C", "X", "Y", "Z", "Q", "R"]
Bad_Systems = ["N", "B", "H", "F", "P"]

#system - quality#
Neural_Best = ["X", "Y", "Z", "Q", "R"]
Best_Systems = ["M", "K"]
Above_Avg_Systems = ["I", "L", "C", "N"]
Below_Avg_Systems = ["B", "H", "F"]
Poor_Systems = ["P"]

#system - family#
Neural = ["X", "Y", "Z", "Q", "R"]
Hybrid = ["M", "K"]
Unit_Sel = ["B", "L", "N"]
HMM = ["C", "H", "I", "F", "P"]

#sysfam-crosstype#
Neural_MR = ["X"]
Neural_WN = ["Y", "Z"]
Neural_GA = ["Q", "R"]

HMM_AbAvg = ["I", "C"]
UnitSel_AbAvg = ["L", "N"]

HMM_BlAvg = ["H", "F", "P"]
UnitSel_BlAvg = ["B"]

############ Add columns ############

New_ColNames = "Manner\tVoicing\tPlace\tSibilance\tPosteriority"
def add_columns(sys_X, name_sys):
	# Send in the DF read by Pandas
    conditions_manner = (sys_X["Phoneme"].isin(Stops), sys_X["Phoneme"].isin(Affricates), sys_X["Phoneme"].isin(Fricatives))
    values_manner = ['Stop', 'Affricate', 'Fricative']
    sys_X['Manner'] = np.select(conditions_manner, values_manner)

    conditions_voicing = (sys_X["Phoneme"].isin(Voiced), sys_X["Phoneme"].isin(Voiceless))
    values_voicing = ['Voiced', 'Voiceless']
    sys_X['Voicing'] = np.select(conditions_voicing, values_voicing)

    conditions_place = (sys_X["Phoneme"].isin(Bilabial), sys_X["Phoneme"].isin(Dental), sys_X["Phoneme"].isin(Labiodental), sys_X["Phoneme"].isin(Alveolar), sys_X["Phoneme"].isin(Postalveolar), sys_X["Phoneme"].isin(Velar), sys_X["Phoneme"].isin(Glottal))
    values_place = ['Bilabial', 'Dental', 'Labiodental', 'Alveolar', 'Postalveolar', 'Velar', 'Glottal']
    sys_X['Place'] = np.select(conditions_place, values_place)

    conditions_sibilance = (sys_X["Phoneme"].isin(Sibilants), sys_X["Phoneme"].isin(Non_Sibilants))
    values_sibilance = ['Sibilant', 'Non_Sibilant']
    sys_X['Sibilance'] = np.select(conditions_sibilance, values_sibilance)

    conditions_posteriority = (sys_X["Phoneme"].isin(Anterior), sys_X["Phoneme"].isin(Posterior))
    values_posteriority = ['Anterior', 'Posterior']
    sys_X['Posteriority'] = np.select(conditions_posteriority, values_posteriority)
    
    sys_X = sys_X.assign(Sys_Name = name_sys)
    sys_X = sys_X.assign(Context = seq_type)   
    
    conditions_quality_baseline = (sys_X["Sys_Name"].isin(Natural), sys_X["Sys_Name"].isin(Good_Systems), sys_X["Sys_Name"].isin(Bad_Systems))
    values_quality_baseline = ['Natural', 'Good', 'Bad']
    sys_X['Sys_Quality_BL'] = np.select(conditions_quality_baseline, values_quality_baseline)
    
    conditions_quality_MK = (sys_X["Sys_Name"].isin(Natural), sys_X["Sys_Name"].isin(Neural_Best), sys_X["Sys_Name"].isin(Best_Systems), sys_X["Sys_Name"].isin(Above_Avg_Systems), sys_X["Sys_Name"].isin(Below_Avg_Systems), sys_X["Sys_Name"].isin(Poor_Systems))
    values_quality_MK = ['Natural', 'Neu-R1', 'R1', 'R2', 'R3', 'R4']
    sys_X['Sys_Quality'] = np.select(conditions_quality_MK, values_quality_MK)

    conditions_type = (sys_X["Sys_Name"].isin(Natural), sys_X["Sys_Name"].isin(Hybrid), sys_X["Sys_Name"].isin(Unit_Sel), sys_X["Sys_Name"].isin(HMM), sys_X["Sys_Name"].isin(Neural))
    values_type = ['Natural', 'Hybrid', 'UnitSel', 'HMM', 'Neural']
    sys_X['Sys_Family'] = np.select(conditions_type, values_type)
    
    ### This is the final Grouping Scheme that was chosen - everything above will be turned off. 
    conditions_cross_type = (sys_X["Sys_Name"].isin(Natural), sys_X["Sys_Name"].isin(Hybrid), sys_X["Sys_Name"].isin(UnitSel_AbAvg), sys_X["Sys_Name"].isin(UnitSel_BlAvg), sys_X["Sys_Name"].isin(HMM_AbAvg), sys_X["Sys_Name"].isin(HMM_BlAvg), sys_X["Sys_Name"].isin(Neural_MR), sys_X["Sys_Name"].isin(Neural_WN), sys_X["Sys_Name"].isin(Neural_GA))
    values_cross_type = ['Natural', 'Hybrid-R1', 'UnitSel-R2', 'UnitSel-R3', 'HMM-R2', 'HMM-R3', 'Neural-MR', 'Neural-WN', 'Neural-GA']
    sys_X['Sys_CrossType'] = np.select(conditions_cross_type, values_cross_type)
    print(sys_X)
    return sys_X

def modify_durationals(name_sys):
    sys_name = '../indiv_feat_files/C.Sys.' + name_sys + '.Duration.Obstruents.' + seq_type + '.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/C.Sys.' + name_sys + '.Duration.Obstruents.' + seq_type + '_newCols.txt', sep='\t', index=False)

def modify_amplitudinals(name_sys):
    sys_name = '../indiv_feat_files/C.Sys.' + name_sys + '.Amplitude.Obstruents.' + seq_type + '.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/C.Sys.' + name_sys + '.Amplitude.Obstruents.' + seq_type + '_newCols.txt', sep='\t', index=False)

def modify_spectrals(name_sys):
    sys_name = '../indiv_feat_files/C.Sys.' + name_sys + '.Spectrals.Obstruents.' + seq_type + '.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/C.Sys.' + name_sys + '.Spectrals.Obstruents.' + seq_type + '_newCols.txt', sep='\t', index=False)


modify_amplitudinals(system_name)
modify_durationals(system_name)
modify_spectrals(system_name)






