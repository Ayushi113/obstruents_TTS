import pandas as pd 
import os
list_systems = ["A", "Q", "R", "Y", "Z"]

######## consonants - VC and CV ########

duration_cons_cv = [pd.read_csv("../indiv_feat_files/" + fil, sep = "\t") for fil in os.listdir("../indiv_feat_files/") if fil.endswith(".Duration.Obstruents.CV_newCols.txt")]
duration_cons_cv_df = pd.concat(duration_cons_cv)
duration_cons_cv_df.to_csv('../text_data/C.01.Duration.All.Systems.CV.txt', sep='\t', index=False)


amplitude_cons_cv = [pd.read_csv("../indiv_feat_files/" + fil, sep = "\t") for fil in os.listdir("../indiv_feat_files/") if fil.endswith(".Amplitude.Obstruents.CV_newCols.txt")]
amplitude_cons_cv_df = pd.concat(amplitude_cons_cv)
amplitude_cons_cv_df.to_csv('../text_data/C.02.Amplitude.All.Systems.CV.txt', sep='\t', index=False)


spectrals_cons_cv = [pd.read_csv("../indiv_feat_files/" + fil, sep = "\t") for fil in os.listdir("../indiv_feat_files/") if fil.endswith(".Spectrals.Obstruents.CV_newCols.txt")]
spectrals_cons_cv_df = pd.concat(spectrals_cons_cv)
spectrals_cons_cv_df.to_csv('../text_data/C.03.Spectrals.All.Systems.CV.txt', sep='\t', index=False)


