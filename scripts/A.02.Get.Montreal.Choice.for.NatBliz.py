#source:https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

import string, re
import tgt, os
from operator import itemgetter 
source_textgrids = '../../Complete_Dataset/output_montreal_1stpass/A_1stpass/'
MFA_textgrids = [tg for tg in os.listdir(source_textgrids) if tg.endswith('.TextGrid')]

RawBliz = open('../../Complete_Dataset/raw_blizzard_data/raw.Bliz.data.txt').read().splitlines()

RawBliz = [re.sub(r'[^\w\s0-9\']',' ',line) for line in RawBliz]
Bliz_WordList = []
for line in RawBliz:
    line = line.split(' ')
    for word in line:
        if word.lower() not in Bliz_WordList:
           Bliz_WordList.append(word.lower())    

Bliz_lexicon = []
for tg in MFA_textgrids:
    print(tg)
    tg_n = source_textgrids + tg
    tg_n = tgt.read_textgrid(tg_n)
    words_tier = tg_n.get_tier_by_name('sentence - words')
    words_tier = [wd for wd in words_tier if wd.text != 'spn']
    words_tier = [wd for wd in words_tier if wd.text != 'sil']
    phones_tier = tg_n.get_tier_by_name('sentence - phones')
    for wd in words_tier:
        start = wd.start_time
        end = wd.end_time
        word_phones = phones_tier.get_annotations_between_timepoints(start, end, left_overlap=False, right_overlap=False)
        phone_seq = [ph.text for ph in word_phones]
        Bliz_lexicon.append(wd.text+'\t'+' '.join(phone_seq))
Disambiguate = []

frequencies = {}

for item in Bliz_lexicon:
    if item in frequencies:
        frequencies[item] += 1
    else:
        frequencies[item] = 1
mult_dict = {}
for key, val in frequencies.items():
	wd = key.split('\t')[0]
	if wd not in mult_dict.keys():
	   mult_dict[wd] = [key.split('\t')[1]+'\t'+str(val)]
	elif wd in mult_dict.keys():
		 mult_dict[wd].append(key.split('\t')[1]+'\t'+str(val))
disambiguated_prons = []
for key1, val1 in mult_dict.items():
	print(key1)
	pron = [pr.split('\t') for pr in mult_dict[key1]]
	if len(mult_dict[key1]) == 1:
	   selected_pron = pron[0][0]
	   disambiguated_prons.append(key1+'\t'+selected_pron)
	elif len(mult_dict[key1]) > 1:
	     pron = [pr.split('\t') for pr in mult_dict[key1]]
	     pron = sorted(pron, key = itemgetter(1), reverse = True)
	     selected_pron = pron[0][0]
	     disambiguated_prons.append(key1+'\t'+selected_pron)
	    
print(len(mult_dict.keys()), len(set(Bliz_WordList)))
print([wd for wd in Bliz_WordList if wd not in mult_dict.keys()])
with open('../text_data/03.Blizzard.Lexicon.No.Variation.txt', 'w') as outFile:
	for lex in sorted(disambiguated_prons):
		outFile.write(lex)
		outFile.write('\n')

