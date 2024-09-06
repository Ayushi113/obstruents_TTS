import tgt, os
import sys
from copy import deepcopy

System = sys.argv[1]
#TextGridDir = '../sample_data/' + System + '/textgrids/'
TextGridDir = '../../Complete_Dataset/output_montreal/' + System + '/01.textgrids_MFA/'
# change system name: 
VarianceFile = open('../indiv_feat_files/V.Optimized.Ceiling.' + System + '.txt').read().splitlines()
fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]
obstruents = fricatives + stops

vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']

ListWords = []

for tgx in os.listdir(TextGridDir):
    textgrid = TextGridDir + tgx
    print(textgrid)
    tg = tgt.read_textgrid(textgrid)

    word_tier = tg.get_tier_by_name('sentence - words')
    phoneme_tier = tg.get_tier_by_name('sentence - phones')

    for idx_w, word in enumerate(word_tier):

        word_start = word.start_time
        word_end = word.end_time
        phone_seq = phoneme_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=True, right_overlap=True)

        for idx_p, ph in enumerate(phone_seq):
            sequence_type = 'NA' #initialize CV, VC and CVC as NA
            if ph.text in vowels and len(phone_seq) == 2: ## don't consider 1-length words
               if idx_p == 0 and phone_seq[idx_p+1].text in obstruents: ## words like "it"
                  sequence_type = "VC"

               elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1].text in obstruents: ## words like "to"
                    sequence_type = "CV"
                    print("num1", word.text, phone_seq, idx_p)

            elif ph.text in vowels and len(phone_seq) > 2: ## words like "can", "its"
                 if idx_p == 0 and phone_seq[idx_p+1].text in obstruents:
                    sequence_type = "VC"

                 elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1].text in obstruents:
                      sequence_type = "CV"
                      print("num2", word.text, phone_seq, idx_p)

                 elif idx_p < len(phone_seq)-1:
                      print(idx_p)
                      if phone_seq[idx_p-1].text in obstruents and phone_seq[idx_p+1].text not in obstruents: # think "can", but not enough
                         if idx_p-1 == -1:
                            sequence_type = "NA"
                            print("would have been a problem")

                         else:
                            sequence_type = "CV"
                            print("num3", word.text, phone_seq, idx_p)

                      elif phone_seq[idx_p-1].text in obstruents and phone_seq[idx_p+1].text in obstruents: # think "cat"
                           sequence_type = "CVC"

                      elif phone_seq[idx_p-1].text not in obstruents and phone_seq[idx_p+1].text in obstruents:
                           sequence_type = "VC"

            else:
                print("Not a vowel!")
            print(sequence_type)
            #print(ph.text, word.text, idx_p, idx_w)
            ListWords.append([tgx.replace('.TextGrid', ''), ph.text, word.text, idx_p, idx_w, sequence_type])
print("Length of list words")
print(len(ListWords))

VarianceFile = [entry.split('\t') for entry in VarianceFile]
VarianceFile, Title = VarianceFile[1:], VarianceFile[0]


ListWords = sorted(ListWords, key=lambda x: (x[0]))

numZeros = len(VarianceFile) - len(ListWords)

for i in range(numZeros):
    ListWords.append([0,0,0]) ## appending zeros for sp, sil etc.

print("Length of list words after appending")
print(len(ListWords))

for idx, row in enumerate(VarianceFile):
    if row[1] == 'sil'or row[1] == 'sp' or row[1] == '':
       ListWords.pop()

       new_entry = [VarianceFile[idx][0], row[1]]
       new_entry.extend(['SIL', 'NA', 'NA', 'NA'])
       ListWords.insert(idx, new_entry)

    else:
        continue

print('\n\n\n\n')
#exit(0)
for idx, (row1, row2) in enumerate(zip(VarianceFile, ListWords)):
    print(row1, row2)
    if row1[1] == row2[1] and len(row1[1]) != 0: #or row1[1][:-1] == row2[1][:-1] 
       row1.insert(1, row2[2])

       if row1[2] not in vowels:
          row1.extend(['NA']*24) # this is a brutally hard-coded line
          row1.extend([row2[3], row2[4], row2[5]])

       elif row1[2] in vowels:
            row1.extend([row2[3], row2[4], row2[5]])

    elif row1[1] != row2[1]:
        print("Error...")
        print("They're not equal")
        print(VarianceFile[idx], ListWords[idx], idx)
        exit(0)

for idx, row in enumerate(VarianceFile):
    if row[-1] == 'CVC':
       new_row = deepcopy(row)
       new_row[-1] = "VC"
       VarianceFile.insert(idx+1, new_row)
       row[-1] = "CV"

Title.insert(1, "Word")

Title.extend(['Phoneme_Index', 'Word_Index', 'Sequence_Type'])

for entry in VarianceFile:
    print(entry, len(entry), len(Title))
    print('\n\n')
#change system here:

with open('../indiv_feat_files/V.Optimized.Ceiling.' + System + '.Wordlabel.txt', 'w') as outFile:
    outFile.write('\t'.join(Title))
    outFile.write('\n')
    for entry in VarianceFile:
        entry = [str(en) for en in entry]
        outFile.write('\t'.join(entry))
        outFile.write('\n')
print("Done! :)")


