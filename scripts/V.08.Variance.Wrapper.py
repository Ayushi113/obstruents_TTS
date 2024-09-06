#usr/env/bin/python3
import subprocess
import os, sys
A = '5000'
B = '0.9'
system_name = sys.argv[1]
inp_dir = "../data/" + system_name + "/08.formants_and_variances/"

vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']
for filename in os.listdir(inp_dir):
    inp = inp_dir + filename
    outp = os.path.splitext(inp)[0].replace('Results-', 'Variances-') + '.txt'    
    subprocess.run(['Rscript', 'V.07.Get.Formant.Variances.R', inp, outp])
    
