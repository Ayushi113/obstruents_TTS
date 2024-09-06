#source: https://stackoverflow.com/questions/11505071/add-specific-value-to-a-data-frame-column-by-matching-a-pattern
## Read in speaker 1
library(stringr)
library("dplyr")
library(lme4)
input = commandArgs(TRUE)
#input1 = '/home/ayushi/Projects_2020/Naturalness/obstruents_and_vowels/data/A/07.formants_and_variances/Results-4500.txt'
FormantsData = read.csv(input[1], sep = '\t', header = TRUE, na.strings="")
Vowels = c('AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2','AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2','IH0', 'IH1', 'IH2','IY0', 'IY1', 'IY2','UH0', 'UH1', 'UH2','UW0', 'UW1', 'UW2')
Dipthongs = c('AW0', 'AW1', 'AW2','AY0', 'AY1', 'AY2','EY0', 'EY1', 'EY2','OW0', 'OW1', 'OW2')
length(colnames(FormantsData))
FormantsData$SegmentType = case_when((FormantsData$TextGridLabel %in% Vowels) ~ 'Vowel', (FormantsData$TextGridLabel %in% Dipthongs) ~ 'Dipthong', TRUE ~ "Consonant")
FormantsData = mutate(FormantsData, LeftContext = lag(TextGridLabel))
FormantsData = mutate(FormantsData, RightContext = lead(TextGridLabel))
FormantsData$StressType = case_when((str_sub(FormantsData$TextGridLabel, -1)) == '1' ~ 'Primary', (str_sub(FormantsData$TextGridLabel, -1)) == '2' ~ 'Secondary', (str_sub(FormantsData$TextGridLabel, -1)) == '0' ~ 'Unstressed', TRUE ~ "CN")
length(colnames(FormantsData))
FormantsData$Vowel.WO.Stress = sub("[012]$", "", FormantsData$TextGridLabel)
col_order = c("Filename","TextGridLabel","Vowel.WO.Stress", "StressType", "SegmentType","LeftContext", "RightContext", "Duration", "F0_onset","F1_onset","F2_onset","F3_onset","F3_band_onset","F5_onset","F5_band_onset", "F1_midpoint", "F2_midpoint","F3_midpoint", "F3_band_midpoint", "F5_midpoint", "F5_band_midpoint", "F0_offset", "F1_offset", "F2_offset", "F3_offset", "F3_band_offset", "F5_offset", "F5_band_offset")

FormantsDataST = FormantsData[, col_order]
FormantsDataST[, 1:28] = sapply(FormantsDataST[, 1:28], as.character) 
FormantsDataST[, 8:28] = sapply(FormantsDataST[, 8:28], as.double) 
FormantsDataST[, 8:28] = round(FormantsDataST[, 8:28], 2)

Mean.F1 = data.frame(aggregate(FormantsDataST$F1_midpoint~FormantsDataST$Vowel.WO.Stress, data=FormantsDataST, mean))
Variance.F1 = data.frame(aggregate(FormantsDataST$F1_midpoint~FormantsDataST$Vowel.WO.Stress, data=FormantsDataST, sd))
Mean.F2 = data.frame(aggregate(FormantsDataST$F2_midpoint~FormantsDataST$Vowel.WO.Stress, data=FormantsDataST, mean))
Variance.F2 = data.frame(aggregate(FormantsDataST$F2_midpoint~FormantsDataST$Vowel.WO.Stress, data=FormantsDataST, sd))


Mean.Var = data.frame(Mean.F1$FormantsDataST.Vowel.WO.Stress, Mean.F1$FormantsDataST.F1_midpoint, Variance.F1$FormantsDataST.F1_midpoint, Mean.F2$FormantsDataST.F2_midpoint, Variance.F2$FormantsDataST.F2_midpoint)
names(Mean.Var) <- c("Vowels", "F1.Mean", "F1.StDev", "F2.Mean", "F2.StDev")
#output = '/home/ayushi/Projects_2020/Naturalness/Current.Workspace/formants_and_variances/A/Variances-4500.txt'
write.table(Mean.Var, file = input[2], row.names=FALSE, sep="\t")
