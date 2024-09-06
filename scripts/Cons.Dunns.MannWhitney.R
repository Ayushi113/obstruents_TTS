setwd("/home/ayushi/ayushi_new/experiments_speechify/speechify/scripts")
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

dunn_test_results = CV_Merged %>% group_by(Manner, Voicing) %>% dunn_test(Spectral.Tilt ~ Sys.Name, p.adjust.method = "BH", detailed = FALSE)
View(dunn_test_results[dunn_test_results$group1=='A',])

whitney_test_results = CV_Merged %>% group_by(Manner, Voicing) %>% wilcox_effsize(Spectral.Tilt ~ Sys.Name)
View(whitney_test_results[whitney_test_results$group1=='A',])
