import subprocess, sys
from multiprocessing import Pool
sys_name = sys.argv[1]
def run_praat(cel):
    subprocess.run(['praat', 'V.05.Formants.With.Ceiling.praat', cel, sys_name])


A = '5000'
B = '0.9'
nb_thread = 5

lis_ceilings = map(str, list(range(4500, 6510, 10))) # excludes last value
with Pool(nb_thread) as p:
     p.map(run_praat, lis_ceilings)



# vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', # 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']

    
