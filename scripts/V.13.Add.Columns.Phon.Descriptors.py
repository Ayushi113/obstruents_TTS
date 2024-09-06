### Script provides functionality for adding new columns (low/high separated formant files as input - output filename+_newCols.txt)
### All other family/ranks combinations are switched off, only RANKSxFAMILY remains.

import pandas as pd, os, sys
import numpy as np

system_name = sys.argv[1]
formant_prefix = 'V.System.' + system_name
input_file_list = sorted([fil for fil in os.listdir('../indiv_feat_files/') if fil.startswith(formant_prefix) and fil.endswith("Formants.txt")])

############ Descriptors of consonants ############
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

############ Descriptors of vowels ############
### 
'''     Front    Central   Back
Low     AE,EH      AA       AO
Mid               AH,ER
High    IH,IY             UH,UW
'''
Vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2','AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2','IH0', 'IH1', 'IH2','IY0', 'IY1', 'IY2','UH0', 'UH1', 'UH2','UW0', 'UW1', 'UW2']
Dipthongs = ['AW0', 'AW1', 'AW2','AY0', 'AY1', 'AY2','EY0', 'EY1', 'EY2','OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2']


High_vowels = ['IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']
Low_vowels = ['AA0', 'AA1', 'AA2', 'AO0','AO1', 'AO2','AE0', 'AE1', 'AE2','EH0', 'EH1', 'EH2']
Medial_vowels = ['AH0', 'AH1', 'AH2', 'ER0', 'ER1', 'ER2']

Front_vowels = ['IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2','AE0', 'AE1', 'AE2','EH0', 'EH1', 'EH2']
Back_vowels = ['UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2', 'AO0','AO1', 'AO2', 'AA0', 'AA1', 'AA2']
Central_vowels = ['AH0', 'AH1', 'AH2', 'ER0', 'ER1', 'ER2']


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


############ Column addition ############
New_ColNames = "Manner\tVoicing\tPlace\tSibilance\tPosteriority\tV.Type\tV.Height\tV.Frontness"
def add_columns(sys_X, name_sys):
	# Send in the DF read by Pandas
    conditions_height = (sys_X["Vowel"].isin(High_vowels), sys_X["Vowel"].isin(Low_vowels), sys_X["Vowel"].isin(Medial_vowels))
    values_vheight = ['High', 'Low', 'Medial']
    sys_X['Vowel_Height'] = np.select(conditions_height, values_vheight)

    conditions_frontness = (sys_X["Vowel"].isin(Front_vowels), sys_X["Vowel"].isin(Back_vowels), sys_X["Vowel"].isin(Central_vowels))
    values_vfrontness = ['Front', 'Back', 'Central']
    sys_X['Vowel_Frontness'] = np.select(conditions_frontness, values_vfrontness)

    conditions_vtype = (sys_X["Vowel"].isin(Vowels), sys_X["Vowel"].isin(Dipthongs))
    values_vtype = ['Vowel', 'Dipthong']
    sys_X['Vowel_Type'] = np.select(conditions_vtype, values_vtype)

    conditions_manner = (sys_X["Obstruent"].isin(Stops), sys_X["Obstruent"].isin(Affricates), sys_X["Obstruent"].isin(Fricatives))
    values_manner = ['Stop', 'Affricate', 'Fricative']
    sys_X['Manner'] = np.select(conditions_manner, values_manner)

    conditions_voicing = (sys_X["Obstruent"].isin(Voiced), sys_X["Obstruent"].isin(Voiceless))
    values_voicing = ['Voiced', 'Voiceless']
    sys_X['Voicing'] = np.select(conditions_voicing, values_voicing)

    conditions_place = (sys_X["Obstruent"].isin(Bilabial), sys_X["Obstruent"].isin(Dental), sys_X["Obstruent"].isin(Labiodental), sys_X["Obstruent"].isin(Alveolar), sys_X["Obstruent"].isin(Postalveolar), sys_X["Obstruent"].isin(Velar), sys_X["Obstruent"].isin(Glottal))
    values_place = ['Bilabial', 'Dental', 'Labiodental', 'Alveolar', 'Postalveolar', 'Velar', 'Glottal']
    sys_X['Place'] = np.select(conditions_place, values_place)

    conditions_sibilance = (sys_X["Obstruent"].isin(Sibilants), sys_X["Obstruent"].isin(Non_Sibilants))
    values_sibilance = ['Sibilant', 'Non_Sibilant']
    sys_X['Sibilance'] = np.select(conditions_sibilance, values_sibilance)

    conditions_posteriority = (sys_X["Obstruent"].isin(Anterior), sys_X["Obstruent"].isin(Posterior))
    values_posteriority = ['Anterior', 'Posterior']
    sys_X['Posteriority'] = np.select(conditions_posteriority, values_posteriority)
    
    sys_X = sys_X.assign(Sys_Name = name_sys)    
    
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
    sys_name = '../indiv_feat_files/V.Sys.' + name_sys + '.Duration.Vowels.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    sys_X.rename(columns = {'Phoneme':'Vowel'}, inplace = True)
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/V.Sys.' + name_sys + '.Duration.Vowels_newCols.txt', sep='\t', index=False)

def modify_amplitudinals(name_sys):
    sys_name = '../indiv_feat_files/V.Sys.' + name_sys + '.Amplitude.Vowels.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    sys_X.rename(columns = {'Phoneme':'Vowel'}, inplace = True)
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/V.Sys.' + name_sys + '.Amplitude.Vowels_newCols.txt', sep='\t', index=False)

def modify_spectrals(name_sys):
    sys_name = '../indiv_feat_files/V.Sys.' + name_sys + '.Spectrals.Vowels.txt'
    sys_X = pd.read_csv(sys_name, sep = "\t")
    sys_X.rename(columns = {'Phoneme':'Vowel'}, inplace = True)
    modified_sys_X = add_columns(sys_X, name_sys)

    modified_sys_X.to_csv('../indiv_feat_files/V.Sys.' + name_sys + '.Spectrals.Vowels_newCols.txt', sep='\t', index=False)

def modify_formants(name_sys, frm_filename):
    sys_name = '../indiv_feat_files/' + frm_filename
    sys_X = pd.read_csv(sys_name, sep = "\t")
    sys_X.rename(columns={'TextGridLabel':'Vowel'}, inplace=True)
    if frm_filename.split('.')[4] == "CV":
       sys_X.rename(columns={'LeftContext':'Obstruent'}, inplace=True)
    elif frm_filename.split('.')[4] == "VC":
         sys_X.rename(columns={'RightContext':'Obstruent'}, inplace=True)
    modified_sys_X = add_columns(sys_X, name_sys)
    modified_sys_X.to_csv(sys_name.replace('.txt', '_newCols.txt'), sep='\t', index=False)

modify_durationals(system_name)
modify_amplitudinals(system_name)
modify_spectrals(system_name)

for frm_file in input_file_list:
    modify_formants(system_name, frm_file)
