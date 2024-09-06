library(stringr)
library("dplyr")
library(lme4)
setwd('/home/ayushi/Projects_2020/Naturalness/organized_InterSpeech_2022/scripts/')
Sys_Name = commandArgs(TRUE)
input_file = paste("../indiv_feat_files/V.Optimized.Ceiling.", Sys_Name, ".Wordlabel.txt", sep ='')
FormantsData = read.csv(input_file, sep = '\t', header = TRUE, na.strings="")
#View(FormantsData)
Vowels = c('AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2','AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2','IH0', 'IH1', 'IH2','IY0', 'IY1', 'IY2','UH0', 'UH1', 'UH2','UW0', 'UW1', 'UW2')
Dipthongs = c('AW0', 'AW1', 'AW2','AY0', 'AY1', 'AY2','EY0', 'EY1', 'EY2','OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2')

FormantsData$SegmentType = case_when((FormantsData$TextGridLabel %in% Vowels) ~ 'Vowel', (FormantsData$TextGridLabel %in% Dipthongs) ~ 'Dipthong', TRUE ~ "Consonant")
FormantsData = mutate(FormantsData, LeftContext = lag(TextGridLabel))
FormantsData = mutate(FormantsData, RightContext = lead(TextGridLabel))
FormantsData$StressType = case_when((str_sub(FormantsData$TextGridLabel, -1)) == '1' ~ 'Primary', (str_sub(FormantsData$TextGridLabel, -1)) == '2' ~ 'Secondary', (str_sub(FormantsData$TextGridLabel, -1)) == '0' ~ 'Unstressed', TRUE ~ "CN")
colnames(FormantsData)
FormantsData$Vowel.WO.Stress = sub("[012]$", "", FormantsData$TextGridLabel)

col_order = c("Filename","Word", "Word_Index", "TextGridLabel", "Phoneme_Index", "Vowel.WO.Stress", "StressType", "SegmentType","LeftContext", "RightContext", "Sequence_Type", "Duration", "F0_onset","F1_onset","F2_onset","F3_onset","F3_band_onset", "F4_onset", "F5_onset","F5_band_onset", "F1_midpoint", "F2_midpoint","F3_midpoint", "F3_band_midpoint", "F4_midpoint", "F5_midpoint", "F5_band_midpoint", "F0_offset", "F1_offset", "F2_offset", "F3_offset", "F3_band_offset", "F4_offset", "F5_offset", "F5_band_offset", "Ceiling")

FormantsDataST = FormantsData[, col_order]
FormantsDataST[, 1:36] = sapply(FormantsDataST[, 1:36], as.character) 
FormantsDataST[, 12:36] = sapply(FormantsDataST[, 12:36], as.double) 
FormantsDataST[, 12:36] = round(FormantsDataST[, 12:36], 2)
# Separated the data into CV and VC contexts; extract onset-midpoint columns with CV; midpoint-offset with VC

FormantsDataST_CV = FormantsDataST[ which(FormantsDataST$Sequence_Type =='CV'),]
FormantsDataST_CV_Onset = cbind(data.frame(FormantsDataST_CV[, 1:12]), FormantsDataST_CV[,grepl(("_onset|_midpoint"), colnames(FormantsDataST_CV))])
FormantsDataST_VC = FormantsDataST[ which(FormantsDataST$Sequence_Type =='VC'),]
FormantsDataST_VC_Offset = cbind(data.frame(FormantsDataST_VC[, 1:12]), FormantsDataST_VC[,grepl("_offset|_midpoint", colnames(FormantsDataST_CV))])

#3. Then, separated into lower and higher formants 

FormantsDataST_CV_Onset_Lower = cbind(data.frame(FormantsDataST_CV_Onset[, 1:12]), FormantsDataST_CV_Onset[,grepl(("F0|F1|F2"), colnames(FormantsDataST_CV_Onset))])

FormantsDataST_CV_Onset_Higher = cbind(data.frame(FormantsDataST_CV_Onset[, 1:12]), FormantsDataST_CV_Onset[,grepl(("F3|F4|F5"), colnames(FormantsDataST_CV_Onset))])

FormantsDataST_VC_Offset_Lower = cbind(data.frame(FormantsDataST_VC_Offset[, 1:12]), FormantsDataST_VC_Offset[,grepl(("F0|F1|F2"), colnames(FormantsDataST_VC_Offset))])

FormantsDataST_VC_Offset_Higher = cbind(data.frame(FormantsDataST_VC_Offset[, 1:12]), FormantsDataST_VC_Offset[,grepl(("F3|F4|F5"), colnames(FormantsDataST_VC_Offset))])

output_cv_onset_lower = paste("../indiv_feat_files/V.System.", Sys_Name, ".Onset.CV.Lower.Formants.txt", sep ='')
output_cv_onset_higher = paste("../indiv_feat_files/V.System.", Sys_Name, ".Onset.CV.Higher.Formants.txt", sep ='')
output_vc_offset_lower = paste("../indiv_feat_files/V.System.", Sys_Name, ".Offset.VC.Lower.Formants.txt", sep ='')
output_vc_offset_higher = paste("../indiv_feat_files/V.System.", Sys_Name, ".Offset.VC.Higher.Formants.txt", sep ='')

write.table(FormantsDataST_CV_Onset_Lower, file = output_cv_onset_lower, row.names=FALSE, sep="\t", quote = FALSE)
write.table(FormantsDataST_CV_Onset_Higher, file = output_cv_onset_higher, row.names=FALSE, sep="\t", quote = FALSE)
write.table(FormantsDataST_VC_Offset_Lower, file = output_vc_offset_lower, row.names=FALSE, sep="\t", quote = FALSE)
write.table(FormantsDataST_VC_Offset_Higher, file = output_vc_offset_higher, row.names=FALSE, sep="\t", quote = FALSE)
