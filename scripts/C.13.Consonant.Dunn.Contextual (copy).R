setwd("/home/ayushi/Projects_2020/Naturalness/organized_InterSpeech_2022/scripts/")
#install.packages("itertools")
library(dplyr)
library(ggpubr)
library(tidyverse)
library(glue)
library(rstatix)
library(itertools)
library(arsenal)

CV_Merged = read.csv("../text_data/C.04.Merged.Consonants.CV.txt", sep = '\t', header = TRUE, na.strings = "")
VC_Merged = read.csv("../text_data/C.04.Merged.Consonants.VC.txt", sep = '\t', header = TRUE, na.strings = "")

group_types = c("Sys.Name", "Sys.Fam", "Sys.Qual", "Sys.Fam.CrossType")
features_for_analyses = c("Consonant_Duration", "Noise_Duration", "RMS_Amplitude", "Peak.Amplitude", "Peak.Frequency", "Dyn.Amplitude", "Spectral.Tilt", "Spectral.Shape")

output_file_prefix = "../DTR_files/voiced_consonants/C.DTR"

for (group in group_types) {
    Group_Results = data.frame(matrix(ncol = 13, nrow = 0))
    for (feature in features_for_analyses) {
        #print(feature)
        dunn_test_results = CV_Merged %>% group_by(Manner, Voicing) %>% dunn_test(formula=eval(parse(text=glue("{feature}~{group}"))), p.adjust.method = "BH", detailed = FALSE)
        dunn_test_results = as.data.frame(dunn_test_results)
        #View(dunn_test_results)
        dunn_test_results$mean_diff = "NA"
        dunn_test_results$median_diff = "NA"
        
        
        for (comp_item in (1:nrow(dunn_test_results))){
            
            reference = dunn_test_results$group1[comp_item]
            target = dunn_test_results$group2[comp_item]
            context = toString(dunn_test_results$Manner[comp_item])
            voice = toString(dunn_test_results$Voicing[comp_item])
            
            ##### MEAN DIFFERENCE IS WRONGGGG!!!! UPDATE FOR VOICINGGGGG!!!!!
            subset_manner_reference = CV_Merged[which(CV_Merged[["Manner"]] == context &  CV_Merged[["Voicing"]] == voice & CV_Merged[[group]] == reference),]
            subset_manner_target = CV_Merged[which(CV_Merged[["Manner"]] == context &  CV_Merged[["Voicing"]] == voice & CV_Merged[[group]] == target),]


            mean_difference = mean(subset_manner_target[[feature]], na.rm=TRUE) - mean(subset_manner_reference[[feature]], na.rm=TRUE)
            median_difference = median(subset_manner_target[[feature]], na.rm=TRUE) - median(subset_manner_reference[[feature]], na.rm=TRUE)
            dunn_test_results$mean_diff[comp_item] = round(mean_difference, 2)
            dunn_test_results$median_diff[comp_item] = round(median_difference, 2)
            #CV_Merged %>% group_by(Manner, reference)         
        }
        Group_Results = rbind(Group_Results, dunn_test_results)        
}

output = paste(output_file_prefix, group, "CV.txt", sep="_")
print(output)
message = paste("Writing to file about", group)
print(message)
write.table(Group_Results, file = output, row.names=FALSE, sep="\t")

}

'''
feature_to_analyse = "Rel_Amp_F4"
group_type = "Sys.Fam.CrossType"
formula_1 = "CV_Merged[[feature_to_analyse]] ~ CV_Merged[[group_type]]"
formula_2 = CV_Merged[[group_type]]
#mod_formula = paste0('velocity_day_', to, ' ~ velocity_day_', from)
library(glue)
#CV_Merged = ungroup(CV_Merged)
dunn_test_results = CV_Merged %>% group_by(Manner) %>% dunn_test(formula=eval(parse(text=glue("{feature_to_analyse}~{group_type}"))), p.adjust.method = "BH", detailed = FALSE)
#dunn_test_results

dunn_test_indivsys = dunn_test_results[which(dunn_test_results$group1=='Natural' & (dunn_test_results$group2=='HMM-R2' | dunn_test_results$group2=='HMM-R3')),]
dunn_test_indivsys

#pairwise_mean = Combined_VowelData_CV %>% group_by(Sys.Name) %>%  summarise_at(vars(Rel_Amp_F5), funs(median(., na.rm=TRUE), mean(., na.rm=TRUE)))
#pairwise_mean
'''





group_types = c("Sys.Name", "Sys.Fam", "Sys.Qual", "Sys.Fam.CrossType")
features_for_analyses = c("Consonant_Duration", "Noise_Duration", "RMS_Amplitude", "Peak.Amplitude", "Peak.Frequency", "Dyn.Amplitude", "Spectral.Tilt", "Spectral.Shape")

output_file_prefix = "../DTR_files/voiced_consonants/C.DTR"

for (group in group_types) {
    Group_Results = data.frame(matrix(ncol = 13, nrow = 0))
    for (feature in features_for_analyses) {
        #print(feature)
        dunn_test_results = VC_Merged %>% group_by(Manner, Voicing) %>% dunn_test(formula=eval(parse(text=glue("{feature}~{group}"))), p.adjust.method = "BH", detailed = FALSE)
        dunn_test_results = as.data.frame(dunn_test_results)
        #View(dunn_test_results)
        dunn_test_results$mean_diff = "NA"
        dunn_test_results$median_diff = "NA"
        
        
        for (comp_item in (1:nrow(dunn_test_results))){
            
            reference = dunn_test_results$group1[comp_item]
            target = dunn_test_results$group2[comp_item]
            context = toString(dunn_test_results$Manner[comp_item])            
            voice = toString(dunn_test_results$Voicing[comp_item])           
            
            subset_manner_reference = VC_Merged[which(VC_Merged[["Manner"]] == context &  VC_Merged[["Voicing"]] == voice & VC_Merged[[group]] == reference),]
            subset_manner_target = VC_Merged[which(VC_Merged[["Manner"]] == context &  VC_Merged[["Voicing"]] == voice & VC_Merged[[group]] == target),]

            
            mean_difference =  mean(subset_manner_target[[feature]], na.rm=TRUE) - mean(subset_manner_reference[[feature]], na.rm=TRUE)
            median_difference = median(subset_manner_target[[feature]], na.rm=TRUE) - median(subset_manner_reference[[feature]], na.rm=TRUE)
            dunn_test_results$mean_diff[comp_item] = round(mean_difference, 2)
            dunn_test_results$median_diff[comp_item] = round(median_difference, 2)
            #VC_Merged %>% group_by(Manner, reference)         
        }
        Group_Results = rbind(Group_Results, dunn_test_results)        
}

output = paste(output_file_prefix, group, "VC.txt", sep="_")
print(output)
message = paste("Writing to file about", group)
print(message)
write.table(Group_Results, file = output, row.names=FALSE, sep="\t")

}

'''
dur_isl = read.csv("../text_data/04.C.Duration.All.Systems.isolate.txt", sep = '\t', header = TRUE, na.strings = "")
amp_isl = read.csv("../text_data/05.C.Amplitude.All.Systems.isolate.txt", sep = '\t', header = TRUE, na.strings = "")
spec_isl = read.csv("../text_data/06.C.Spectrals.All.Systems.isolate.txt", sep = '\t', header = TRUE, na.strings = "")
colnames(spec_isl)
identity_cols <- c("Filename", "Word.Index", "Word", "Phoneme.Index", "Phoneme", "Sys_Name")

## Create a unique field using ^^ identity_cols
SortUniqueId <- function(df) {
    df$UnID = do.call(paste, c(df[identity_cols], sep = "-"))
    df = df[order(df$UnID),]
}

Duration_ISL = SortUniqueId(dur_isl)
Amplitude_ISL = SortUniqueId(amp_isl)
Spectrals_ISL = SortUniqueId(spec_isl)
#summary(Amplitude_ISL)
#### Merge the data ##
Merged_VowelData_ISL = Reduce(merge, list(Duration_ISL, Amplitude_ISL, Spectrals_ISL))

summary(Merged_VowelData_ISL$Sys_Name) ## This is important to see if all the systems have the same number of data points

### Display all the column names with their indices
iname = enumerate(colnames(Merged_VowelData_ISL))
#cat(sapply(iname, function(n) sprintf("%d -> %s\n", n$index, n$value)), sep = "")

ISL_Merged = Merged_VowelData_ISL
iname = enumerate(colnames(ISL_Merged))
#cat(sapply(iname, function(n) sprintf("%d -> %s\n", n$index, n$value)), sep = "")

summary(ISL_Merged$Sys_Family)
cols_to_update = c("Sys_Family","Sys_Quality", "Sys_CrossType")
ISL_Merged[cols_to_update] = sapply(ISL_Merged[cols_to_update], as.character)
#sapply(ISL_Merged, class)

#1. Family
ISL_Merged$Sys_Family[ISL_Merged$Sys_Name == "X"] <- "Neural-MR"
ISL_Merged$Sys_Family[ISL_Merged$Sys_Name == "Y" | ISL_Merged$Sys_Name == "Z"] <- "Neural-WN"

ISL_Merged$Sys_Family[ISL_Merged$Sys_Family == "HMM_WP"] <- "HMM"
ISL_Merged$Sys_Family[ISL_Merged$Sys_Family == "HMM_P"] <- "HMM"
ISL_Merged$Sys_Family = as.factor(ISL_Merged$Sys_Family)
print(summary(ISL_Merged$Sys_Family))

#2. Quality
ISL_Merged$Sys_Quality[ISL_Merged$Sys_Quality == "0"] <- "Neural"
ISL_Merged$Sys_Quality = as.factor(ISL_Merged$Sys_Quality)
print(summary(ISL_Merged$Sys_Quality))

#3. CrossType
#ISL_Merged$Sys_CrossType[ISL_Merged$Sys_CrossType == "0"] <- "Neural"
ISL_Merged$Sys_CrossType[ISL_Merged$Sys_Name == "X"] <- "Neural-MR"
ISL_Merged$Sys_CrossType[ISL_Merged$Sys_Name == "Y" | ISL_Merged$Sys_Name == "Z"] <- "Neural-WN"

ISL_Merged$Sys_CrossType = as.factor(ISL_Merged$Sys_CrossType)
print(summary(ISL_Merged$Sys_CrossType))
#############################################

ISL_Merged$Sys.Fam = factor(ISL_Merged$Sys_Family, levels = c("Natural", "Hybrid", "UnitSel", "HMM", "Neural-MR", "Neural-WN"))

ISL_Merged$Sys.Name = factor(ISL_Merged$Sys_Name, levels = c("A", "M", "K", "I", "C", "L", "N", "H", "F", "B", "P", "X", "Y", "Z"))

ISL_Merged$Sys.Qual = factor(ISL_Merged$Sys_Quality, levels = c("Natural","R1","R2","R3","R4", "Neural"))

ISL_Merged$Sys.Fam.CrossType = factor(ISL_Merged$Sys_CrossType, levels = (c("Natural","Hybrid-R1","UnitSel-R2","UnitSel-R3","HMM-R2","HMM-R3", "HMM-R4", "Neural-MR", "Neural-WN")))


#ISL_Merged_mP = subset(ISL_Merged, Sys.Name != "P")
#ISL_Merged_mDipCons = subset(ISL_Merged, SegmentType == "Vowel")
#ISL_Merged = droplevels(ISL_Merged_mDipCons)
#colnames(ISL_Merged)
iname = enumerate(colnames(ISL_Merged))
#cat(sapply(iname, function(n) sprintf("%d -> %s\n", n$index, n$value)), sep = "")
#summary(ISL_Merged)
'''

'''
group_types = c("Sys.Name", "Sys.Fam", "Sys.Qual", "Sys.Fam.CrossType")
features_for_analyses = c("Consonant_Duration", "Noise_Duration", "RMS_Amplitude", "Peak.Amplitude", "Peak.Frequency", "Dyn.Amplitude", "Spectral.Tilt", "Spectral.Shape")

output_file_prefix = "../text_data/DTR_files/voiced_consonants/C.DTR"

for (group in group_types) {
    Group_Results = data.frame(matrix(ncol = 13, nrow = 0))
    for (feature in features_for_analyses) {
        #print(feature)
        dunn_test_results = ISL_Merged %>% group_by(Manner, Voicing) %>% dunn_test(formula=eval(parse(text=glue("{feature}~{group}"))), p.adjust.method = "BH", detailed = FALSE)
        dunn_test_results = as.data.frame(dunn_test_results)
        #View(dunn_test_results)
        dunn_test_results$mean_diff = "NA"
        dunn_test_results$median_diff = "NA"
        
        
        for (comp_item in (1:nrow(dunn_test_results))){
            
            reference = dunn_test_results$group1[comp_item]
            target = dunn_test_results$group2[comp_item]
            context = toString(dunn_test_results$Manner[comp_item])
            
            voice = toString(dunn_test_results$Voicing[comp_item])           
            
            ##### MEAN DIFFERENCE IS WRONGGGG!!!! UPDATE FOR VOICINGGGGG!!!!!##### MEAN DIFFERENCE IS WRONGGGG!!!! UPDATE FOR VOICINGGGGG!!!!!
            subset_manner_reference = ISL_Merged[which(ISL_Merged[["Manner"]] == context &  ISL_Merged[["Voicing"]] == voice & ISL_Merged[[group]] == reference),]
            subset_manner_target = ISL_Merged[which(ISL_Merged[["Manner"]] == context &  ISL_Merged[["Voicing"]] == voice & ISL_Merged[[group]] == target),]
            
            mean_difference =  mean(subset_manner_target[[feature]], na.rm=TRUE) - mean(subset_manner_reference[[feature]], na.rm=TRUE)
            median_difference = median(subset_manner_target[[feature]], na.rm=TRUE) - median(subset_manner_reference[[feature]], na.rm=TRUE)
            dunn_test_results$mean_diff[comp_item] = round(mean_difference, 2)
            dunn_test_results$median_diff[comp_item] = round(median_difference, 2)
            #ISL_Merged %>% group_by(Manner, reference)         
        }
        Group_Results = rbind(Group_Results, dunn_test_results)        
}

output = paste(output_file_prefix, group, "ISL.txt", sep="_")
print(output)
message = paste("Writing to file about", group)
print(message)
write.table(Group_Results, file = output, row.names=FALSE, sep="\t")

}
'''
