import tgt, os, sys
import numpy as np

sys_name = sys.argv[1]
cont = sys.argv[2]

fricatives_context = ["fricatives_CV", "fricatives_VC", "fricatives_isolate"]
plosives_context = ["stops_CV", "stops_VC", "stops_isolate"]
affricate_context = ["affricates_CV", "affricates_VC", "affricates_isolate"]

list_contexts = [context for context in fricatives_context if context.endswith(cont)] + [context for context in plosives_context if context.endswith(cont)] + [context for context in affricate_context  if context.endswith(cont)]
print(list_contexts)
input_dirc = "../data/" + sys_name + "/06.context_separation_consonants/" 

consonantal_info = []

for context in list_contexts:
    input_dir = input_dirc + context + '/'

    if context in affricate_context or context in plosives_context:
       closure_dir = input_dir + "stops_with_closure/"
       noise_dir = input_dir + "noise_region_stops/"

       closure_textgrids = sorted([tgt for tgt in os.listdir(closure_dir) if tgt.endswith(".TextGrid")])
       noise_textgrids = sorted([tgt for tgt in os.listdir(noise_dir) if tgt.endswith(".TextGrid")])
       
       #booksent_2013_0044_19_just_0_JH.TextGrid
       for cl_tgt, ns_tgt in zip(closure_textgrids, noise_textgrids):
           closure_tgt = tgt.io.read_textgrid(closure_dir + cl_tgt)
           noise_tgt = tgt.io.read_textgrid(noise_dir + ns_tgt)
           phoneme_tier = closure_tgt.get_tier_by_name('sentence - phones')
           noise_tier = noise_tgt.get_tier_by_name('sentence - noise')

           consonant_duration = (phoneme_tier.end_time - phoneme_tier.start_time) * 1000
           noise_duration = (noise_tier.end_time - noise_tier.start_time) * 1000
           closure_duration = (consonant_duration - noise_duration) * 1000

           sentence = '_'.join([cl_tgt.split('_')[0], cl_tgt.split('_')[1], cl_tgt.split('_')[2]])
           idx_w = cl_tgt.split('_')[3]
           word = cl_tgt.split('_')[4]
           idx_p = cl_tgt.split('_')[5]
           phoneme = cl_tgt.split('_')[6]

           cons_info = sentence + '\t' + str(idx_w) + '\t' + word + '\t' + str(idx_p) + '\t' + phoneme.replace('.TextGrid', '') + '\t' + str(consonant_duration) + '\t' + str(closure_duration) + '\t' + str(noise_duration)
           consonantal_info.append(cons_info)

    elif context in fricatives_context:
         noise_dir = input_dir
         noise_textgrids = sorted([tgt for tgt in os.listdir(noise_dir) if tgt.endswith(".TextGrid")])

       #booksent_2013_0044_19_just_0_JH.TextGrid
         for ns_tgt in noise_textgrids:
             print(ns_tgt)
             noise_tgt = tgt.io.read_textgrid(noise_dir + ns_tgt)
             noise_tier = noise_tgt.get_tier_by_name('sentence - phones')

             consonant_duration = (noise_tier.end_time - noise_tier.start_time) * 1000
             noise_duration = consonant_duration
             closure_duration = 0.0

             sentence = '_'.join([ns_tgt.split('_')[0], ns_tgt.split('_')[1], ns_tgt.split('_')[2]])
             idx_w = ns_tgt.split('_')[3]
             word = ns_tgt.split('_')[4]
             idx_p = ns_tgt.split('_')[5]
             phoneme = ns_tgt.split('_')[6]

             cons_info = sentence + '\t' + str(idx_w) + '\t' + word + '\t' + str(idx_p) + '\t' + phoneme.replace('.TextGrid', '') + '\t' + str(consonant_duration) + '\t' + str(closure_duration) + '\t' + str(noise_duration)
             consonantal_info.append(cons_info)


Title_consonants = "Filename\tWord-Index\tWord\tPhoneme-Index\tPhoneme\tConsonant_Duration\tClosure_Duration\tNoise_Duration\n"

with open("../indiv_feat_files/C.Sys." + sys_name + ".Duration.Obstruents." + cont + ".txt", 'w') as outFile1:
    outFile1.write(Title_consonants)
    for inf in consonantal_info:
        outFile1.write(inf)
        outFile1.write('\n')



