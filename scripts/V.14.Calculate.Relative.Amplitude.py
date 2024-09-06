import sys
import numpy as np
import scipy
from scipy import signal
import scipy.io.wavfile
#import matplotlib.pyplot as plt
import sys,os,re, random
import python_speech_features
import librosa
import statistics, math
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import random
import pandas as pd
sys_name = sys.argv[1]
context = sys.argv[2]

fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]
obstruents = fricatives + stops


if context == 'VC':
   input_file = '../indiv_feat_files/V.System.' + sys_name + ".Offset." + context + '.Higher.Formants_newCols.txt'
   vowel_directory = '../data/' + sys_name + '/07.vowels/V1_VC/'
   F3_region = "F3_offset"
   F3_band_region = "F3_band_offset"
   F4_region = "F4_offset"
   F4_band_region = "F4_band_offset"
   F5_region = "F5_offset"
   F5_band_region = "F5_band_offset"
elif context == 'CV':     
     input_file = '../indiv_feat_files/V.System.' + sys_name + ".Onset." + context + '.Higher.Formants_newCols.txt'     
     vowel_directory = '../data/' + sys_name + '/07.vowels/V2_CV/'
     F3_region = "F3_onset"
     F3_band_region = "F3_band_onset"
     F4_region = "F4_onset"
     F4_band_region = "F4_band_onset"
     F5_region = "F5_onset"
     F5_band_region = "F5_band_onset"
     

input_formants = pd.read_csv(input_file, sep = '\t')
input_formants["Rel_Amp_F3"] = "NaN"
input_formants["Rel_Amp_F4"] = "NaN"
input_formants["Rel_Amp_F5"] = "NaN"
obstruent_formants = input_formants.loc[input_formants['Obstruent'].isin(obstruents)]

stop_directory = '../data/' + sys_name + '/04.noise_region_stops/'

fricative_directory = '../data/' + sys_name + '/05.fricatives/'



def takeClosest(num,collection): 
    # source: https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
   return min(collection,key=lambda x:abs(x-num))

## Passing a signal through a filter
def butter_highpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    y = signal.filtfilt(b, a, data)
    return y

def preprocess_signal(raw_signal):
    # Filtering and pre-emphasis
    filter_sig = python_speech_features.sigproc.preemphasis(raw_signal, coeff=0.97)
    filter_sig = butter_highpass_filter(filter_sig, 200, 16000, order=5)
    return filter_sig


def get_spectral_features(SR, filtered_signal, bandwidth, formant):
    Final_amplitude = 0.0
    if np.isnan(formant):
       print("Here's somthin")
       Final_amplitude = np.nan
       return Final_amplitude
    ########### Basic Features for everywhere ############
    Signal_FFT_Abs = np.abs(librosa.stft(filtered_signal, center=True, n_fft=512, window='hamm', hop_length=320, dtype=np.complex64)) # 10 ms overlap       
    
    Associated_Freqs = librosa.fft_frequencies(sr=16000, n_fft=512)
    FFT_amplitude_dB = librosa.amplitude_to_db(Signal_FFT_Abs)
    
    Target_Formant = takeClosest(formant, Associated_Freqs)


    Formant_Min, Formant_Max = takeClosest((Target_Formant - 50), Associated_Freqs), takeClosest((Target_Formant + 50), Associated_Freqs)
    Formant_Min_ID, Formant_Max_ID = np.where(Associated_Freqs == Formant_Min)[0][0], np.where(Associated_Freqs == Formant_Max)[0][0]
    FFT_dB_reqrange = FFT_amplitude_dB[Formant_Min_ID:Formant_Max_ID]

    Mean_Amplitude_Overall = np.mean(FFT_dB_reqrange, axis=1) # mean across samples
    Final_amplitude = np.mean(Mean_Amplitude_Overall, axis=0)

    return Final_amplitude



for idx in obstruent_formants.index.values: # don't iterate over row numbers cuz wtf PandaS! 
    if obstruent_formants.loc[idx, "Obstruent"] in stops:
       consonant_directory = stop_directory
    elif obstruent_formants.loc[idx, "Obstruent"] in fricatives:
        consonant_directory = fricative_directory
    else:
        print("Doesn't look like an obstruent CV to me!")
        print(obstruent_formants.loc[idx])
        sys.exit(0)


    vowel_cues = [obstruent_formants.loc[idx, "Filename"], obstruent_formants.loc[idx, "Obstruent"],
        obstruent_formants.loc[idx, "Word_Index"],    obstruent_formants.loc[idx, "Word"],  obstruent_formants.loc[idx, "Phoneme_Index"],obstruent_formants.loc[idx, "Vowel"]]

    if context == "CV":    
       consonant_cues = [obstruent_formants.loc[idx, "Filename"], obstruent_formants.loc[idx, "Word_Index"], obstruent_formants.loc[idx, "Word"], obstruent_formants.loc[idx, "Phoneme_Index"]-1,obstruent_formants.loc[idx, "Obstruent"]]
    elif context == "VC":
         consonant_cues = [obstruent_formants.loc[idx, "Filename"], obstruent_formants.loc[idx, "Word_Index"], obstruent_formants.loc[idx, "Word"], obstruent_formants.loc[idx, "Phoneme_Index"]+1,obstruent_formants.loc[idx, "Obstruent"]]

    target_F3 = obstruent_formants.loc[idx, F3_region]
    target_F3_band = obstruent_formants.loc[idx, F3_band_region]

    target_F4 = obstruent_formants.loc[idx, F4_region]
    target_F4_band = target_F3_band

    target_F5 = obstruent_formants.loc[idx, F5_region]
    target_F5_band = obstruent_formants.loc[idx, F5_band_region]
    print(target_F3, target_F5, type(target_F5), "checkin`")
    print("\n\n")

    consonant_wavFile = consonant_directory + '_'.join([str(en) for en in consonant_cues]) + '.wav'
    consonant_TextGrid = consonant_directory + '_'.join([str(en) for en in consonant_cues]) + '.TextGrid'

    vowel_wavFile = vowel_directory + '_'.join([str(en) for en in vowel_cues]) + '.wav'
    vowel_TextGrid = vowel_directory + '_'.join([str(en) for en in vowel_cues]) + '.TextGrid' 

    #SR_cons, consonant_wav = scipy.io.wavfile.read(consonant_wavFile)
    Cons_Amp_F3, Cons_Amp_F4, Cons_Amp_F5 = 0.0, 0.0, 0.0
    Vowel_Amp_F3, Vowel_Amp_F4, Vowel_Amp_F5 = 0.0, 0.0, 0.0


    if os.path.exists(consonant_wavFile) and os.path.exists(consonant_TextGrid):
       print("Consonant -- waveFile and Textgrid exist")
       SR_cons, consonant_wav = scipy.io.wavfile.read(consonant_wavFile)       
       filtered_consonant = preprocess_signal(consonant_wav)
       ## reversing consonant in CV
       if context == "CV":      
          reverse_filtered_consonant = filtered_consonant[::-1] #reverse consonant if CV [--C--][--V--]. We need the latter portion [C--]. 
       elif context == "VC":
            reverse_filtered_consonant = filtered_consonant
       
       #padding is common for both stops & fricatives because it's the transition boundary under consideration. 
       # 00 + [revCt--revCs] + V || V + 00 + [Cs--Ct]. 
       # window is centered on revCt for CV and Cs for VC. That's where the transition is! 
       padded_filtered_consonant = np.pad(reverse_filtered_consonant, (len(reverse_filtered_consonant), 0), constant_values=(0)) 
       
       
       ### I'm learning that reversal is not needed. will really have to look through this whole code again. ### 
       Cons_Amp_F3 = get_spectral_features(SR_cons, padded_filtered_consonant, target_F3_band, target_F3)
       Cons_Amp_F4 = get_spectral_features(SR_cons, padded_filtered_consonant, target_F4_band, target_F4)
       Cons_Amp_F5 = get_spectral_features(SR_cons, padded_filtered_consonant, target_F5_band, target_F5)
       print("Amplitude F3 consonant = ", Cons_Amp_F3)
       print("Amplitude F3 consonant = ", Cons_Amp_F4)
       print("Amplitude F5 consonant = ", Cons_Amp_F5)

    else:
        print("Consonant - a file maybe missing!")
        print(consonant_wavFile, consonant_TextGrid)
        continue        
 
    if os.path.exists(vowel_wavFile) and os.path.exists(vowel_TextGrid):
       print("Vowel-- waveFile and Textgrid exist")
       SR_vowel, vowel_wav = scipy.io.wavfile.read(vowel_wavFile)

       filtered_vowel = preprocess_signal(vowel_wav)
       ## reversing vowel in VC
       if context == "CV":
          filtered_vowel = filtered_vowel
       elif context == "VC":
            filtered_vowel = filtered_vowel[::-1]
       padded_filtered_vowel = np.pad(filtered_vowel, (len(filtered_vowel), 0), constant_values=(0))
       Vowel_Amp_F3 = get_spectral_features(SR_vowel, padded_filtered_vowel, target_F3_band, target_F3)
       Vowel_Amp_F4 = get_spectral_features(SR_vowel, padded_filtered_vowel, target_F4_band, target_F4)
       Vowel_Amp_F5 = get_spectral_features(SR_vowel, padded_filtered_vowel, target_F5_band, target_F5)
       print("Amplitude F3 vowel = ", Vowel_Amp_F3)
       print("Amplitude F4 vowel = ", Vowel_Amp_F4)
       print("Amplitude F5 vowel = ", Vowel_Amp_F5)

    else:
        print("Vowel - a file maybe missing!")
        print(vowel_wavFile, vowel_TextGrid)

    Relative_Amplitude_F3 = Cons_Amp_F3 - Vowel_Amp_F3 # this is correct - check Pg 146 Redmon's
    Relative_Amplitude_F4 = Cons_Amp_F4 - Vowel_Amp_F4
    Relative_Amplitude_F5 = Cons_Amp_F5 - Vowel_Amp_F5
    input_formants.loc[input_formants.index[idx], 'Rel_Amp_F3'] = Relative_Amplitude_F3
    input_formants.loc[input_formants.index[idx], 'Rel_Amp_F4'] = Relative_Amplitude_F4
    input_formants.loc[input_formants.index[idx], 'Rel_Amp_F5'] = Relative_Amplitude_F5
    
    print("Relative amplitudes are:-")
    print("F3 ", Relative_Amplitude_F3)
    print("F4 ", Relative_Amplitude_F4)
    print("F5", Relative_Amplitude_F5)
    

input_formants.to_csv(input_file.replace('.txt', '_RA.txt'), sep = '\t')
