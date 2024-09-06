#source: https://stackoverflow.com/questions/49363247/how-to-combine-multiple-lists-into-one-using-first-element-of-each-list-as-key
import os,sys
from collections import defaultdict
system_name = sys.argv[1]
# For 1 speaker:
#InpDir = '../sample_data/' + inp + '/formants_and_variances/variances/'
InpDir = '../data/' + system_name + '/08.formants_and_variances/'
Var_Files = [fil for fil in os.listdir(InpDir) if fil.startswith("Variances-")]
print(Var_Files)
# For multispeaker:
# InpDir = '../formants_and_variances/Timit.Perfect.To.Formants/' + inp + '/variances/'

ListVowels = ["AA","AE","AH","AO","AW","AY","EH","ER","EY","IH","IY","OW","OY","UH","UW"]
resVar = []
for fi in Var_Files:
    fil = InpDir + fi
    resFile = open(fil).read().splitlines()
    #print("Title line:", resFile[0].split('\t'))
    resFile = resFile[1:] #leave starting line out
    for entry in resFile:
        print(entry)
        entry = entry.split('\t')
        entry = [en.replace('NA', '5000') if en == 'NA' else en for en in entry]
        entry = [st.replace('"','') if st == entry[0] else round(float(st),2) for st in entry]
        print(entry)
        entry.append(fi)
        resVar.append(entry)

resDict = {}

for line in resVar:
    if line[0] in resDict:
        resDict[line[0]].append(line[1:])
    else:
        resDict[line[0]] = [line[1:]]

for vowel, feats in resDict.items():
    print(vowel, feats)
    feats = sorted(feats, key=lambda x:(x[3], x[1]))
    print(feats)
    feats = [[vowel] + feat for feat in feats]
    resDict[vowel] = '\n'.join(['\t'.join(map(str, feat)) for feat in feats])

print(resDict)
# For 1 speaker:
outp= '../indiv_feat_files/V.Sorted.Variances.' + system_name + '.txt'

# For multi speaker:
#outp= '../text_data/timit.sorted.files' + inp + '.Sorted.txt'

with open(outp, 'w') as f:
    [f.write('{0}\n\n'.format(value)) for key, value in resDict.items()]
