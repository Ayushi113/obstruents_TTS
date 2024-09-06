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
print(len(vowels_dir))
#exit(0)

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

Spectral_Features = []

def get_spectral_features(SR, filtered_signal, hop_length):

    ########### Basic Features for everywhere ############
    Signal_FFT_Abs = np.abs(librosa.stft(filtered_signal, center=True, n_fft=512, window='hamm', hop_length=160, dtype=np.complex64)) # 10 ms overlap       
    
    Associated_Freqs = librosa.fft_frequencies(sr=16000, n_fft=512)
    FFT_amplitude_dB = librosa.amplitude_to_db(Signal_FFT_Abs)
    

    Associated_freqs_noSource = Associated_Freqs[18:]
    ####### Spectral Peak and Amplitude  ###########
 
    FFT_dB_noSource = FFT_amplitude_dB[18:] # Removing source characteristics - only 550 Hz+ ==> 18:
    Mean_Amplitude_Overall = np.mean(FFT_dB_noSource, axis=1) # mean across samples

    AMP_PK = np.max(Mean_Amplitude_Overall, axis=0) # mean amplitude across frequencies

    ################### Spectral Tilt #####################  

    log_Freqs = np.log10(Associated_freqs_noSource)
    log_Freq_multipFactor = np.vstack([log_Freqs, np.ones(len(log_Freqs))]).T
    Overall_TILT, intercept = np.linalg.lstsq(log_Freq_multipFactor, Mean_Amplitude_Overall, rcond=None)[0]

    
    Spectral_features = [Overall_TILT]
    Spectral_features = [str(np.round(feat, 2)) for feat in Spectral_features]
    return Overall_TILT

Spectral_Measurements = []
for vowel_fil in vowels_dir:
    print(vowel_fil)
     
    type_of_vowel = vowel_fil.split('/')[4]
    print(type_of_vowel)
    #exit(0)
    
    Spectral_Tilt = 0.0
    Context = ''
    hop_length = 320 # 20 ms windows

    if type_of_vowel == "V1_VC":
       
       Context = "VC"
       SR, Vowel_File = scipy.io.wavfile.read(vowel_fil)
       print(Vowel_File)
       #print([type(num) for num in Vowel_File])
       ## Noise region - RMS amplitude
       filtered_vowel = preprocess_signal(Vowel_File)
       print(filtered_vowel)
       reverse_filtered_vowel = filtered_vowel[::-1]
       print(reverse_filtered_vowel)
       #exit(0)
       
       padded_filtered_vowel = np.pad(reverse_filtered_vowel, (len(reverse_filtered_vowel), 0), constant_values=(0))

       Spectral_Tilt = get_spectral_features(SR, padded_filtered_vowel, hop_length)
       
    elif type_of_vowel == "V2_CV":

         Context = "CV"         
         SR, Vowel_File = scipy.io.wavfile.read(vowel_fil)

         filtered_vowel = preprocess_signal(Vowel_File) # no reversal here!
         padded_filtered_vowel = np.pad(filtered_vowel, (len(filtered_vowel), 0), constant_values=(0))

         Spectral_Tilt = get_spectral_features(SR, padded_filtered_vowel, hop_length)
    fil_name = vowel_fil.split('/')[5]     
    info = '_'.join(fil_name.split('_')[0:3]) + '\t' + fil_name.split('_')[3] + '\t' + Context + '\t' + fil_name.split('_')[4] + '\t' + fil_name.split('_')[5] + '\t' + fil_name.split('_')[6] + '\t' + fil_name.split('_')[7].replace(".wav", "") + '\t' + str(np.round(Spectral_Tilt, 2))
    print(info)
    Spectral_Measurements.append(info)
print(len(Spectral_Measurements))
#exit(0)
Title = "Filename\tObstruent\tContext\tWord-Index\tWord\tPhoneme-Index\tPhoneme\tSpectral-Tilt"
with open('../indiv_feat_files/V.Sys.' + System + '.Spectrals.Vowels.txt', 'w') as outFile:
    outFile.write(Title)
    outFile.write('\n')
    for amp_feat in Spectral_Measurements:
        outFile.write(amp_feat)
        outFile.write('\n')

   
