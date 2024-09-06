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
