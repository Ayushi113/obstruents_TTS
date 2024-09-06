setwd("~/Projects_2020/Naturalness/organized_InterSpeech_2022/scripts/")
library(stringr)
library(dplyr)
library(ggplot2)
library(reshape2)
DTR_results = list.files("../DTR_files/voiced_consonants/")
hm_info = read.csv("../text_data/A.04.heatmap_info_noTitle.txt", sep = "\t", header = TRUE)

target_groups = c("M", "K", "C", "I", "L", "N", "Q", "R", "X", "Y", "Z",  "HMM", "HMM-R2", "HMM-R3", "HMM-R4", "Neural-WN", "Neural")
group_name = "HMap_All.Sys"

for (fil in DTR_results) {
  print(fil)
  fil_info = hm_info[which(hm_info$Filename == fil),]
  plot_title = fil_info$Plot_Title[1]
  
  x_label = fil_info$XLabel[1]
  y_label = fil_info$YLabel[1]
  
  x_ordering = unlist(strsplit(as.character(fil_info$Feature_Ordering[1]), " "))
  y_ordering = unlist(strsplit(as.character(fil_info$Group_Ordering[1]), " "))
  
  input_file = fil
  phon_class_context = read.csv(paste("../DTR_files/voiced_consonants/", input_file, sep = ""), header = TRUE, sep = '\t')
  
  phon_class_context$statistic = as.character(phon_class_context$statistic)
  
  phon_class_context$statistic[phon_class_context$p.adj.signif=="ns"]  = "0.0" 
  
  phon_class_context$statistic = as.numeric(phon_class_context$statistic)
  
  grouped_natural_hn = phon_class_context[ which((phon_class_context$group1 == 'Natural' |  phon_class_context$group1 == 'A') & (phon_class_context$group2 %in% target_groups)), ]
  grouped_natural_hn = droplevels(grouped_natural_hn)
  
  grouped_natural_hn = grouped_natural_hn[ !(grouped_natural_hn$.y. == 'Delta_F1' |  grouped_natural_hn$.y. == 'Delta_F2' | grouped_natural_hn$.y. == 'Delta_F3' | grouped_natural_hn$.y. == 'Delta_F4' | grouped_natural_hn$.y. == 'Delta_F5'), ]
  grouped_natural_hn = droplevels(grouped_natural_hn)
  
  grouped_natural_hn = droplevels(grouped_natural_hn)
  
  grouped_natural_hn$.y. = factor(grouped_natural_hn$.y., levels = x_ordering)
  grouped_natural_hn$group2 = factor(grouped_natural_hn$group2, levels = rev(y_ordering))
  View(grouped_natural_hn)
  #results.heatmap = ggplot(data = grouped_natural_hn, mapping = aes(x = .y., y = group2, fill = statistic)) + geom_tile() +  xlab(label = x_label) +  ylab(label = paste(y_label, '\n\n\n\n')) +  scale_fill_gradient2(low = "blue", mid = "white", high = "red") +  facet_grid(Voicing~Manner) + theme(axis.text.x = element_text(angle = 90)) + ggtitle(plot_title)
  results.heatmap = ggplot(data = grouped_natural_hn, mapping = aes(x = .y., y = group2, fill = statistic)) + geom_tile() +  xlab(label = x_label) +  ylab(label = paste(y_label, '\n\n\n\n')) +  scale_fill_gradient2(low = "blue", mid = "white", high = "red") +  facet_grid(Voicing~Manner) + theme(axis.text.x = element_text(angle = 90)) + theme(text = element_text(size = 35)) + labs(fill = "Z-value") ## no title
  print(results.heatmap)
  #break
  
  out_file = str_replace(input_file, "DTR", group_name)
  output_png = paste("../output_plots/voiced_consonants/faceted_manners/", str_replace(out_file, ".txt", ".png"), sep = "") 
  output_pdf = paste("../output_plots/voiced_consonants/faceted_manners/", str_replace(out_file, ".txt", ".pdf"), sep = "")
  
  pdf(output_pdf, width=25, height=18)
  print(results.heatmap)
  dev.off()
  
  results.heatmap.noFacet = ggplot(data = grouped_natural_hn, mapping = aes(x = .y., y = group2, fill = statistic)) + geom_tile() +  xlab(label = x_label) +  ylab(label = paste(y_label, '\n\n\n\n')) +  scale_fill_gradient2(low = "blue", mid = "white", high = "red") + facet_grid(~Voicing) + theme(axis.text.x = element_text(angle = 90)) + ggtitle(plot_title)
  
  output_png_nf = paste("../output_plots/voiced_consonants/all_manners/", str_replace(out_file, ".txt", ".png"), sep = "") 
  output_pdf_nf = paste("../output_plots/voiced_consonants/all_manners/", str_replace(out_file, ".txt", ".pdf"), sep = "")
  
  pdf(output_pdf_nf, width=10)
  print(results.heatmap.noFacet)
  dev.off()
}
