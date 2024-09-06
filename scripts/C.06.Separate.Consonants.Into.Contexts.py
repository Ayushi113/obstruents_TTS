import os,sys
import shutil
System = sys.argv[1]
source_dir_stops = os.listdir("../data/" + System + "/02.stops_with_closure/")
source_dir_fricatives = os.listdir("../data/" + System + "/05.fricatives/")
obstruent_dir = source_dir_stops + source_dir_fricatives
print(len(obstruent_dir))
#exit(0)
source_dir = [fil for fil in obstruent_dir if fil.endswith('.wav')]
lexicon = open("../text_data/A.03.Blizzard.Lexicon.No.Variation.txt").read().splitlines()
lex_dict = {lex.split('\t')[0]:lex.split('\t')[1] for lex in lexicon}
#print(lex_dict)

fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
stops = ["P", "B", "T", "D", "K", "G"]
affricates = ["CH", "JH"]
obstruents = fricatives + stops + affricates
vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']

CV_tokens = 0
VC_tokens = 0
VCV_tokens = 0
isolate_tokens = 0

for fil in source_dir:
    print(fil)
    word = fil.split('_')[4]
    obstruent = fil.split('_')[6]
    obstruent = obstruent.replace('.wav', '')
    destination_add = ''
    if obstruent in fricatives:
       obstruent = "fricative"
       source = "../data/" + System + "/05.fricatives/"
       destination_add = '../data/' + System + '/06.context_separation_consonants/fricatives_'
    elif obstruent in stops:
         obstruent = "stop"
         source = "../data/" + System + "/02.stops_with_closure/"
         destination_add = '../data/' + System + '/06.context_separation_consonants/stops_'
    else:
    	obstruent = "affricate"
    	source = "../data/" + System + "/02.stops_with_closure/"
    	destination_add = '../data/' + System + '/06.context_separation_consonants/affricates_'

    obstruent_id = fil.split('_')[5]
    phone_seq = lex_dict[word].split(' ')
    for idx_p, ph in enumerate(phone_seq):
        destination_dir = ''    
        if str(idx_p) == obstruent_id:
           print(phone_seq)
           print(ph, "is the target phoneme in the word", word)              
           if ph in obstruents and len(phone_seq) == 2: ## don't consider 1-length words
              if idx_p == 0 and phone_seq[idx_p+1] in vowels: ## words like "to"
                 print("Pure CV sequence -- initial\n")
                 CV_tokens = CV_tokens + 1
                 destination_dir = destination_add + 'CV/'
                 print(destination_dir)

              elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1] in vowels:
                   print("Pure VC sequence -- final\n")
                   VC_tokens = VC_tokens + 1
                   destination_dir = destination_add + 'VC/'
                   vowel = phone_seq[idx_p-1]
                   #x_vc_fnl = vowel_output(ph)
                   print(destination_dir)

           elif ph in obstruents and len(phone_seq) > 2: ## words like "can", "cats"
                if idx_p == 0 and phone_seq[idx_p+1] in vowels: ## words like "it"
                   print("Pure CV sequence -- initial\n")
                   CV_tokens = CV_tokens + 1
                   destination_dir = destination_add + 'CV/'
                   vowel = phone_seq[idx_p+1]
                      #x_vc_inl = vowel_output(ph)
                   print(destination_dir)

                elif idx_p == 0 and phone_seq[idx_p+1] not in vowels: ## words like "it"
                   print("Isolate\n")
                   isolate_tokens = isolate_tokens + 1
                   destination_dir = destination_add + 'isolate/'
                   vowel = ''
                   print(destination_dir)

                elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1] in vowels:
                     print("Pure VC sequence -- final\n")
                     VC_tokens = VC_tokens + 1
                     destination_dir = destination_add + 'VC/'
                     vowel = phone_seq[idx_p-1]
                     #x_cv_fnl = vowel_output(ph)
                     print(destination_dir)

                elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1] not in vowels:
                     print("Isolate\n")
                     isolate_tokens = isolate_tokens + 1
                     destination_dir = destination_add + 'isolate/'
                     vowel = ''
                     #x_cv_fnl = vowel_output(ph)
                     print(destination_dir)

                elif idx_p < len(phone_seq)-1:
                     if phone_seq[idx_p-1] in vowels and phone_seq[idx_p+1] not in vowels: # think "can"
                        if idx_p-1 == -1:
                           continue
                        else:
                            print("Pure VC sequence -- medial\n")
                            VC_tokens = VC_tokens + 1
                            destination_dir = destination_add + 'VC/'
                            vowel = phone_seq[idx_p-1]
                            print(destination_dir)
                              #x_cv_mdl = vowel_output(ph)

                     elif phone_seq[idx_p-1] in vowels and phone_seq[idx_p+1] in vowels: # think "cat"
                            print("VCV sequence -- medial\n")
                            VCV_tokens = VCV_tokens + 1
                            destination_dir = destination_add + 'VC/'
                            vowel = phone_seq[idx_p-1]
                            
                            print(destination_dir)
                            shutil.copy(source + fil, destination_dir)
                            shutil.copy(source + fil.replace(".wav", ".TextGrid"), destination_dir)
                             #x_cv_mdl = vowel_output(ph)

                            destination_dir = destination_add + 'CV/'
                            vowel = phone_seq[idx_p+1]
                            print(destination_dir)
                             #x_vc_mdl = vowel_output(ph)

                     elif phone_seq[idx_p-1] not in vowels and phone_seq[idx_p+1] in vowels:
                          print("Pure CV sequence -- medial\n")
                          CV_tokens = CV_tokens + 1
                          destination_dir = destination_add + 'CV/'  ## made this change after InS
                          vowel = phone_seq[idx_p+1]
                          print(destination_dir)
                             #x_cv_mdl = vowel_output(ph)

                     elif phone_seq[idx_p-1] not in vowels and phone_seq[idx_p+1] not in vowels:
                          print("Isolate\n")
                          isolate_tokens = isolate_tokens + 1
                          destination_dir = destination_add + 'isolate/'
                          vowel = ''
                          print(destination_dir)
                             #x_cv_mdl = vowel_output(ph)
           print(destination_dir, "de\n\n")
           shutil.copy(source + fil, destination_dir)
           shutil.copy(source + fil.replace(".wav", ".TextGrid"), destination_dir)
          # else:
          #    print("Not our interest")
print("CV tokens:",  CV_tokens)
print("VC tokens:", VC_tokens)
print("Isolates:", isolate_tokens)


