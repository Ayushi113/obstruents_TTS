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
context = sys.argv[2]
affricates_dir_noise = '../data/' + System + '/06.context_separation_consonants/affricates_' + context + '/noise_region_stops/'
stops_dir_noise = '../data/' + System + '/06.context_separation_consonants/stops_' + context + '/noise_region_stops/'
source_dir_fricatives = '../data/' + System + '/06.context_separation_consonants/fricatives_' + context + '/'

affricate_dir = [fil for fil in os.listdir(affricates_dir_noise) if fil.endswith('.wav')]
stop_dir = [fil for fil in os.listdir(stops_dir_noise) if fil.endswith('.wav')]
fricative_dir = [fil for fil in os.listdir(source_dir_fricatives) if fil.endswith('.wav')]
obstruent_dir = affricate_dir + stop_dir + fricative_dir
print(len(affricate_dir), len(stop_dir), len(fricative_dir))
print(len(obstruent_dir))
#exit(0)
affricates = ["CH", "JH"]
fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
plosives = ["P", "B", "T", "D", "K", "G"]
stops = ["P", "B", "T", "D", "K", "G","CH", "JH"]
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


def cut_with_centering(wave):
    wave_midpoint = []
    if len(wave) <= 640:    # 640 samples = 40 ms
       print("fricative too small..")
       return wave
    else:
       midpoint = len(wave)/2
       midpoint_left, midpoint_right = int(midpoint - 320), int(midpoint + 320)       
       wave_midpoint = wave[midpoint_left:midpoint_right]     
       return wave_midpoint


def get_spectral_features(filtered_signal):

    ########### Basic Features for everywhere ############
    Signal_FFT_Abs = np.abs(librosa.stft(filtered_signal, center=True, n_fft=512, window='hamm', hop_length=160, dtype=np.complex64)) # 10 ms overlap       
    
    Associated_Freqs = librosa.fft_frequencies(sr=16000, n_fft=512)
    FFT_amplitude_dB = librosa.amplitude_to_db(Signal_FFT_Abs)
    

    Associated_freqs_noSource = Associated_Freqs[18:]
    
    ####### Spectral Peak and Amplitude  ###########

    FFT_dB_noSource = FFT_amplitude_dB[18:] # Removing source characteristics - only 550 Hz+ ==> 18:
    Mean_Amplitude_Overall = np.mean(FFT_dB_noSource, axis=1) # mean across samples

    AMP_PK = np.max(Mean_Amplitude_Overall, axis=0) # mean amplitude across frequencies

    Freq_PK_location = [idx for idx, amp in enumerate(Mean_Amplitude_Overall) if amp == np.max(Mean_Amplitude_Overall)][0]
    
    FREQ_PK = Associated_freqs_noSource[Freq_PK_location]

    ################# Dynamic Amplitude ###############
    FFT_db_Trough = FFT_amplitude_dB[0:65] # below 2 kHz
    Mean_Amp_Trough = np.mean(FFT_db_Trough, axis=1)
    Max_Amp_Trough = np.max(Mean_Amp_Trough, axis = 0)
    
    Dynamic_Amplitude = AMP_PK - Max_Amp_Trough 
    
    ################### Spectral Tilt #####################  

    log_Freqs = np.log10(Associated_freqs_noSource)
    log_Freq_multipFactor = np.vstack([log_Freqs, np.ones(len(log_Freqs))]).T
    Overall_TILT, intercept = np.linalg.lstsq(log_Freq_multipFactor, Mean_Amplitude_Overall, rcond=None)[0]
    print(Overall_TILT, intercept)
    print("This is the tilt params..")

    ################## Spectral Shape ####################
    LowFreq_Interval = Associated_freqs_noSource[0:63] # 550 - 2500 Hz
    HighFreq_Interval = Associated_freqs_noSource[63:] # 2500 - 8000 Hz

    LowFreq_Interval = [freq/1000 for freq in LowFreq_Interval]
    HighFreq_Interval = [freq/1000 for freq in HighFreq_Interval]
    
    LowFreq_dB = Mean_Amplitude_Overall[0:63]
    HighFreq_dB = Mean_Amplitude_Overall[63:]

    LowFreq_MultFactor = np.vstack([LowFreq_Interval, np.ones(len(LowFreq_Interval))]).T
    HighFreq_MultFactor = np.vstack([HighFreq_Interval, np.ones(len(HighFreq_Interval))]).T

    LowFreq_TILT, Int_Low = np.linalg.lstsq(LowFreq_MultFactor, LowFreq_dB, rcond=None)[0]
    HighFreq_TILT, Int_High = np.linalg.lstsq(HighFreq_MultFactor, HighFreq_dB, rcond=None)[0]

    Spectral_SHAPE = LowFreq_TILT - HighFreq_TILT
    
    ################### Final output #######################
    Spectral_features = [AMP_PK, FREQ_PK, Dynamic_Amplitude, Overall_TILT, Spectral_SHAPE]
    Spectral_features = [str(np.round(feat, 2)) for feat in Spectral_features]
    return Spectral_features

Spectral_Measurements = []
for obstruent_fil in obstruent_dir:
    print(obstruent_fil)
    obstruent_ph = obstruent_fil.split('_')[6].replace(".wav", "")    
    Spectrals = []    
    source_dir_stops = ""
    if obstruent_ph in stops:
       if obstruent_ph in affricates:
          source_dir_stops = affricates_dir_noise
       elif obstruent_ph in plosives:
            source_dir_stops = stops_dir_noise
       hop_length = 48 # 3 ms windows  

       SR, Stop_File = scipy.io.wavfile.read(source_dir_stops + obstruent_fil)
      
       ## Noise region - RMS amplitude
       filtered_stop = preprocess_signal(Stop_File)       
       padded_filtered_stop = np.pad(filtered_stop, (len(filtered_stop), 0), constant_values=(0))       
       Spectrals = get_spectral_features(padded_filtered_stop)
       
    elif obstruent_ph in fricatives:
         
         hop_length = 160 # 10 ms windows
    
         SR, Fric_File = scipy.io.wavfile.read(source_dir_fricatives + obstruent_fil)
         filtered_signal = preprocess_signal(Fric_File)
         centered_portion = cut_with_centering(filtered_signal)
         Spectrals = get_spectral_features(centered_portion)
    
    info = '_'.join(obstruent_fil.split('_')[0:3]) + '\t' + obstruent_fil.split('_')[3] + '\t' + obstruent_fil.split('_')[4] + '\t' + obstruent_fil.split('_')[5] + '\t' + obstruent_fil.split('_')[6].replace(".wav", "") + '\t' + '\t'.join(Spectrals)
    print(info)
    Spectral_Measurements.append(info)

Title = "Filename\tWord-Index\tWord\tPhoneme-Index\tPhoneme\tPeak.Amplitude\tPeak.Frequency\tDyn.Amplitude\tSpectral.Tilt\tSpectral.Shape"

with open('../indiv_feat_files/C.Sys.' + System + ".Spectrals.Obstruents." + context + ".txt", 'w') as outFile:
     outFile.write(Title)
     outFile.write('\n')
     for spectral in Spectral_Measurements:
         outFile.write(spectral)
         outFile.write('\n')

