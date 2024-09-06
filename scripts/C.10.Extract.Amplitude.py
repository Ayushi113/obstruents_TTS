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
#'../data/' + sys_name + '/03.textgrids_noise/'

affricate_dir_noise = "../data/" + System + "/06.context_separation_consonants/affricates_" + context + "/noise_region_stops/"
affricate_dir_closure = "../data/" + System + "/06.context_separation_consonants/affricates_" + context + "/stops_with_closure/"

stop_dir_noise = "../data/" + System + "/06.context_separation_consonants/stops_" + context + "/noise_region_stops/"
stop_dir_closure = "../data/" + System + "/06.context_separation_consonants/stops_" + context + "/stops_with_closure/"


source_dir_fricatives = "../data/" + System + "/06.context_separation_consonants/fricatives_" + context + "/"

affricate_dir = [fil for fil in os.listdir(affricate_dir_closure) if fil.endswith('.wav')]
stop_dir = [fil for fil in os.listdir(stop_dir_closure) if fil.endswith('.wav')]
fricative_dir = [fil for fil in os.listdir(source_dir_fricatives) if fil.endswith('.wav')]
#print(fricative_dir)
print(len(fricative_dir))
obstruent_dir = affricate_dir + stop_dir + fricative_dir
#print(obstruent_dir)
print(len(obstruent_dir))
#exit(0)
fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]
affricates = ["CH", "JH"]
plosives = ["P", "B", "T", "D", "K", "G"]
def approximate_chunking(a, n):
    # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(a), n)
    chunked = [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
    return chunked

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
       #print("fricative too small..")
       return wave
    else:
       midpoint = len(wave)/2
       midpoint_left, midpoint_right = int(midpoint - 320), int(midpoint + 320)       
       wave_midpoint = wave[midpoint_left:midpoint_right]     
       return wave_midpoint

def get_moving_average(amplitude_in_dB):
    amplitude_in_dB = amplitude_in_dB.tolist()
    slide = 4
    moving_average_results = []
    for idx, val in enumerate(amplitude_in_dB):
        if idx < len(amplitude_in_dB) - slide: 
           portion = amplitude_in_dB[idx:idx+slide]
           mean_portion = np.round((sum(portion)/len(portion)), 2)
           moving_average_results.append([mean_portion, list(range(idx, idx+slide)), portion])

        else:
           continue
    return moving_average_results


def detect_burst(amplitude_in_dB):
    print(amplitude_in_dB)
    moving_average = [avg[0] for avg in get_moving_average(amplitude_in_dB)]
    #print(moving_average)
    
    indices = [avg[1] for avg in get_moving_average(amplitude_in_dB)]
    #print(indices)
    amplitude_vals = [avg[2] for avg in get_moving_average(amplitude_in_dB)]
    location = 0
    burst_amplitude = 0
    peak = 0
    for idx, avg in enumerate(moving_average):        
        if idx <= len(moving_average)-2:
           if moving_average[idx] > moving_average[idx+1]:
              print("Going down.. ", idx)              
           elif moving_average[idx] < moving_average[idx+1]:
                print("Increase detected..")
                if moving_average[idx] > 50:
                   for idx_a, amp in enumerate(amplitude_vals[idx]):
                       if amp > 55:
                          location = indices[idx][idx_a]
                          print("Best peak..")
                          burst_amplitude = np.round(amplitude_vals[idx][idx_a], 2)
                          peak = 1
                          return burst_amplitude, peak
                       elif amp <= 55:
                            no_other_chance = [val for val in moving_average[idx:] if val >= 55]
                            if len(no_other_chance) == 0:
                               max_amp_loc = amplitude_vals[idx].index(max(amplitude_vals[idx]))
                               location = indices[idx][max_amp_loc]
                               print("Not loud peak")
                               ##print(location)
                               peak = 1
                               burst_amplitude = np.round(amplitude_vals[idx][max_amp_loc], 2)
                               return burst_amplitude, peak 

                elif moving_average[idx] <= 50:
                     no_other_chance = [val for val in moving_average[idx:] if val >= 50]
                     if len(no_other_chance) == 0:
                        max_amp_loc = amplitude_vals[idx].index(max(amplitude_vals[idx]))
                        location = indices[idx][max_amp_loc]
                        print("Soft spectrum..")
                        peak = 1
                        burst_amplitude = np.round(amplitude_vals[idx][max_amp_loc], 2)
                        #print(burst_amplitude)
                        
                        return burst_amplitude, peak
                     else:
                         continue

        elif idx == len(moving_average)-1:
             chunks = approximate_chunking(moving_average, 4)
             print(chunks, len(chunks[2]))
             idx = len(moving_average) - len(chunks[2])
             #location = indices[idx][0]
             print(indices, idx, "indice")
             peak = 0
             burst_amplitude = amplitude_vals[idx][2]
             return burst_amplitude, peak


def get_burst_amplitude(sr, signal, hop):
    Fourier_Absolute = np.abs(librosa.stft(signal, center=True, n_fft=512, window='hamm', hop_length=hop_length, dtype=np.complex64))
    Fourier_dB = librosa.amplitude_to_db(Fourier_Absolute)
    
    Mean_across_Freqs = np.mean(Fourier_dB, axis = 0)
    print(Mean_across_Freqs)
    Burst_Amp, Peak_Pres = detect_burst(Mean_across_Freqs)
    return Burst_Amp, Peak_Pres

def get_RMS_amplitude(sr, signal, hop):
    Fourier_Absolute = np.abs(librosa.stft(signal, center=True, n_fft=512, window='hamm', hop_length=hop_length, dtype=np.complex64))
    Fourier_dB = librosa.amplitude_to_db(Fourier_Absolute)
    
    Mean_across_Freqs = np.mean(Fourier_dB, axis = 0)
    RMS_Amplitude = np.sqrt(np.mean(Mean_across_Freqs ** 2))
    return RMS_Amplitude

Amplitude_Features = []
for obstruent_fil in obstruent_dir:
    print(len(obstruent_dir))
    #print('\n\n', obstruent_fil)
    obstruent_ph = obstruent_fil.split('_')[6].replace(".wav", "")    
    
    Burst_amplitude = 0.0
    RMS_amplitude = 0.0
    Peak_Presence = 0
    source_dir_noise = ""
    source_dir_stops = ""
    if obstruent_ph in stops:
       if obstruent_ph in affricates:
          source_dir_noise = affricate_dir_noise
          source_dir_stops = affricate_dir_closure
       elif obstruent_ph in plosives:
            source_dir_noise = stop_dir_noise
            source_dir_stops = stop_dir_closure
       #1. window asymmetrically the raw signal
       #2. calculate RMS amplitude
       #3. calculate burst amplitude
       print(obstruent_ph)
       print(source_dir_noise)

       hop_length = 48 # 3 ms windows  

       SR, Noise_File = scipy.io.wavfile.read(source_dir_noise + obstruent_fil)
       SR, Stop_File = scipy.io.wavfile.read(source_dir_stops + obstruent_fil)
      
       ## Noise region - RMS amplitude
       filtered_noise = preprocess_signal(Noise_File)       
       padded_filtered_noise = np.pad(filtered_noise, (len(filtered_noise), 0), constant_values=(0))       
       RMS_amplitude = get_RMS_amplitude(SR, padded_filtered_noise, hop_length)

       filtered_stop = preprocess_signal(Stop_File)       
       Burst_amplitude, Peak_Presence = get_burst_amplitude(SR, filtered_stop, hop_length)
       print(Burst_amplitude, "Frequency domain")

    elif obstruent_ph in fricatives:
         #1. cut central portion
         #2. window 30 ms from centre; both directions
         #3. calculate RMS amplitude; burst = NA

         hop_length = 160 # 10 ms windows
    
         SR, Fric_File = scipy.io.wavfile.read(source_dir_fricatives + obstruent_fil)
         filtered_signal = preprocess_signal(Fric_File)
         centered_portion = cut_with_centering(filtered_signal)
         RMS_amplitude = get_RMS_amplitude(SR, centered_portion, hop_length)
         Burst_amplitude, Peak_Presence = 0.0, 0

    info = '_'.join(obstruent_fil.split('_')[0:3]) + '\t' + obstruent_fil.split('_')[3] + '\t' + obstruent_fil.split('_')[4] + '\t' + obstruent_fil.split('_')[5] + '\t' + obstruent_fil.split('_')[6].replace(".wav", "") + '\t' + str(RMS_amplitude) + '\t' + str(Burst_amplitude) + '\t' + str(Peak_Presence)
    print(info)
    Amplitude_Features.append(info)

Title = "Filename\tWord-Index\tWord\tPhoneme-Index\tPhoneme\tRMS_Amplitude\tBurst_Amplitude\tPeak_Presence"
Amplitude_Features = random.sample(Amplitude_Features, len(Amplitude_Features))
with open('../indiv_feat_files/C.Sys.' + System + '.Amplitude.Obstruents.' + context + '.txt', 'w') as outFile:
	outFile.write(Title)
	outFile.write('\n')
	for amp_feat in Amplitude_Features:
		outFile.write(amp_feat)
		outFile.write('\n')

   
