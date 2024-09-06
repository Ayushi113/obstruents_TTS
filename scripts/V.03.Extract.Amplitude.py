## AUTHOR: Ayushi Pandey                           ##    
## TASK: Durational measurements for obstruents ##
## MEASUREMENTS: (a) Burst amplitude (if stop) and (b) noise amplitude
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

System = sys.argv[1]

source_dir_VC = '../data/' + System + '/07.vowels/V1_VC/'
source_dir_CV = '../data/' + System + '/07.vowels/V2_CV/'

VC_dir = [source_dir_VC + fil for fil in os.listdir(source_dir_VC) if fil.endswith('.wav')]
CV_dir = [source_dir_CV + fil for fil in os.listdir(source_dir_CV) if fil.endswith('.wav')]
vowels_dir = VC_dir + CV_dir
print(vowels_dir)


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


def get_RMS_amplitude(sr, signal, hop):
    Fourier_Absolute = np.abs(librosa.stft(signal, center=True, n_fft=512, window='hamm', hop_length=hop_length, dtype=np.complex64))
    Fourier_dB = librosa.amplitude_to_db(Fourier_Absolute)
    
    Mean_across_Freqs = np.mean(Fourier_dB, axis = 0)
    RMS_Amplitude = np.sqrt(np.mean(Mean_across_Freqs ** 2))
    return RMS_Amplitude

Amplitude_Features = []

for vowel_fil in vowels_dir:
    print(vowel_fil)
    
    type_of_vowel = vowel_fil.split('/')[4]
    
    RMS_amplitude = 0.0
    Context = ''
    hop_length = 320 # 20 ms windows

    if type_of_vowel == "V1_VC":
       
       Context = "VC"
       SR, Vowel_File = scipy.io.wavfile.read(vowel_fil)
       ## Noise region - RMS amplitude
       filtered_vowel = preprocess_signal(Vowel_File)
       reverse_filtered_vowel = filtered_vowel[::-1]

       padded_filtered_vowel = np.pad(reverse_filtered_vowel, (len(reverse_filtered_vowel), 0), constant_values=(0))       
       RMS_amplitude = get_RMS_amplitude(SR, padded_filtered_vowel, hop_length)
       
    elif type_of_vowel == "V2_CV":

         Context = "CV"         
         SR, Vowel_File = scipy.io.wavfile.read(vowel_fil)

         filtered_vowel = preprocess_signal(Vowel_File)
         padded_filtered_vowel = np.pad(filtered_vowel, (len(filtered_vowel), 0), constant_values=(0))

         RMS_amplitude = get_RMS_amplitude(SR, padded_filtered_vowel, hop_length)
    fil_name = vowel_fil.split('/')[5]     
    info = '_'.join(fil_name.split('_')[0:3]) + '\t' + fil_name.split('_')[3] + '\t' + Context + '\t' + fil_name.split('_')[4] + '\t' + fil_name.split('_')[5] + '\t' + fil_name.split('_')[6] + '\t' + fil_name.split('_')[7].replace(".wav", "") + '\t' + str(np.round(RMS_amplitude, 2))
    print(info)
    Amplitude_Features.append(info)

Title = "Filename\tObstruent\tContext\tWord-Index\tWord\tPhoneme-Index\tPhoneme\tRMS_Amplitude"
with open('../indiv_feat_files/V.Sys.' + System + '.Amplitude.Vowels.txt', 'w') as outFile:
	outFile.write(Title)
	outFile.write('\n')
	for amp_feat in Amplitude_Features:
		outFile.write(amp_feat)
		outFile.write('\n')

   
