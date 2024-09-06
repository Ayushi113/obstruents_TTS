import re
import sys, os
#Change system name for system_nameut file:
system_name = sys.argv[1]
system_nameFile = '../indiv_feat_files/V.Sorted.Variances.' + system_name + '.txt'
ListVariances = open(system_nameFile).read().splitlines()
TopRows = [line for idx, line in enumerate(ListVariances) if ListVariances[idx-1] == '']


#Change system name for file TO BE MODIFIED:
baseFile = '../data/' + system_name +  '/08.formants_and_variances/Results-4500.txt'
fullOutput = open(baseFile).read().splitlines()
#Change system name for system_nameut directory (A, M, P):
system_nameDir = '../data/' + system_name +  '/08.formants_and_variances/'
Var_Files = [fil for fil in os.listdir(system_nameDir) if fil.startswith("Results-")]
for line in TopRows:
    line = line.split('\t')
    vowel, formantData = line[0], line[5].replace('Variances', 'Results')
    ceiling = re.search('Variances-(.*).txt', line[5]).group(1)
    formantFile = open(system_nameDir + formantData).read().splitlines()
    print(len(formantFile), ceiling, vowel)
    for idx, lin in enumerate(formantFile):
        #print(lin, lin.split('\t')[1][:-1], idx)
        if lin.split('\t')[1][:-1] == vowel:
           fullOutput[idx] = lin.strip() + '\t' + ceiling
print(fullOutput)     
fullOutput[0] = fullOutput[0] + '\t' + 'Ceiling'
OutpFile = '../indiv_feat_files/V.Optimized.Ceiling.' + system_name + '.txt'
with open(OutpFile, 'w') as outFile:
    for line in fullOutput:
        outFile.write(line)
        outFile.write('\n')
