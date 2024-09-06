#https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
import tgt
import numpy as np
import scipy
from scipy import signal
import scipy.io.wavfile
import sys,os,re
import python_speech_features
import librosa
from scipy.fftpack import fft, fftshift

System = sys.argv[1]
# SOURCE = LOCATION OF STOPS - PHONEMES (WAV AND TEXTGRID) CHOPPED
source_dir = "../data/" + System + "/02.stops_with_closure/"
# DESTINATION = DIRECTORY WITH EMPTY TEXTGRIDS
noise_textgrid_dir = "../data/" + System + "/03.textgrids_noise/"


def preemphasis(x, coef=0.97):
    # source: https://www.programcreek.com/python/example/55202/scipy.signal.lfilter
    #####print  ("here",x.dtype)
    b = np.array([1., -coef], x.dtype)
    a = np.array([1.], x.dtype)
    return scipy.signal.lfilter(b, a, x) 


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

## Passing a signal through a filter
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]

wav_list = [wav for wav in os.listdir(source_dir) if wav.endswith('.wav')]
grid_list = [grid for grid in os.listdir(source_dir) if grid.endswith('.TextGrid') ]

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

def create_ms_equivalent(sr, signal, hop):
    len_signal = len(signal)
    lower_limit = 0
    hop_in_ms = (hop * 1000) / sr
    if hop_in_ms % 2 == 0:
       lower_limit = int(hop_in_ms/2)
    else:
       lower_limit = int(hop_in_ms/2) + 1

    upper_limit = lower_limit + ((len_signal/hop) - 1)*hop_in_ms
    spacing = round((hop*1000/sr), 0)

    millisec_equivalent = np.arange(lower_limit, upper_limit+hop_in_ms, spacing)
    Fourier_freqs = librosa.fft_frequencies(sr=SR, n_fft=512)
    return millisec_equivalent


def approximate_chunking(a, n):
    # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(a), n)
    chunked = [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
    return chunked


def get_V_shape(amplitude_in_dB):
    moving_average = [avg[0] for avg in get_moving_average(amplitude_in_dB)]
    
    indices = [avg[1] for avg in get_moving_average(amplitude_in_dB)]
    
    amplitude_vals = [avg[2] for avg in get_moving_average(amplitude_in_dB)]
    location = 0
    print(moving_average)
    for idx, avg in enumerate(moving_average):        
        if idx < len(moving_average)-1:
           if moving_average[idx] > moving_average[idx+1]:
              print("Going down.. ", idx)
              if idx == len(moving_average)-2:
                 chunks = approximate_chunking(moving_average, 4)
                 idx = len(moving_average) - len(chunks[2])
                 location = indices[idx][0]
                 print("Tukka")
                 return location
              else:
                 continue
           elif moving_average[idx] < moving_average[idx+1]:
                print("Increase detected..")
                if moving_average[idx] > 50:
                   for idx_a, amp in enumerate(amplitude_vals[idx]):
                       if amp >= 55:
                          location = indices[idx][idx_a]
                          print(location)
                          return location
                       elif amp < 55:
                            #print(amplitude_vals[idx_a:])
                            no_other_chance = [val for val in moving_average[idx:] if val > 55]
                            if len(no_other_chance) == 0:
                               max_amp_loc = amplitude_vals[idx].index(max(amplitude_vals[idx]))
                               location = indices[idx][max_amp_loc]
                               print(location)
                               print("Not a loud peak..")
                               return location 

                elif moving_average[idx] < 50:
                     no_other_chance = [val for val in moving_average[idx:] if val > 50]
                     if len(no_other_chance) == 0:
                        print(amplitude_vals[idx])
                        max_amp_loc = amplitude_vals[idx].index(max(amplitude_vals[idx]))
                        location = indices[idx][max_amp_loc]
                        print(location)
                        print("Perhaps no peak detected..")
                        return location
                     else:
                         continue

        elif idx == len(moving_average)-1:
             chunks = approximate_chunking(moving_average, 4)
             idx = len(moving_average) - len(chunks[2])
             location = indices[idx][0]
             print("burst at end")
             return location

def get_noise_boundary(sr, signal, hop):
    ms_equivalent = create_ms_equivalent(SR, signal, hop)
    Fourier_Absolute = np.abs(librosa.stft(HighP_WavFile, center=True, n_fft=512, window='hamm', hop_length=hop_length, dtype=np.complex64))
    Fourier_dB = librosa.amplitude_to_db(Fourier_Absolute)
    

    # Hard-coded range - 1500 Hz to 5000 Hz
    Fourier_dB_HighFreq = Fourier_dB[49:161]
    Mean_across_Freqs = np.mean(Fourier_dB, axis = 0)
    noise_boundary_location = get_V_shape(Mean_across_Freqs)
    return ms_equivalent[noise_boundary_location]

def create_new_textgrid(wavFile, boundary_point):
    sentence_ = '_'.join(wav.split('_')[0:3]) + '_noise.TextGrid'
    word_position = int(wav.split('_')[3])
    phoneme_position = int(wav.split('_')[5])
    TextGrid = tgt.read_textgrid(noise_textgrid_dir + sentence_)
    words_tier = TextGrid.get_tier_by_name('sentence - words')
    phonemes_tier = TextGrid.get_tier_by_name('sentence - phones')
    noise_tier = TextGrid.get_tier_by_name('sentence - noise')
    
    
    word_start = words_tier[word_position].start_time
    word_end = words_tier[word_position].end_time
    phone_seq = phonemes_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=False, right_overlap=False)
    distance_from_noise_boundary = phone_seq[phoneme_position].start_time
    boundary_start = distance_from_noise_boundary + boundary_point/1000

    boundary_end = phone_seq[phoneme_position].end_time
    boundary_dur = boundary_end - boundary_start
    noise_tier.add_annotation(tgt.Interval(boundary_start, boundary_start + boundary_dur, wav.split('_')[6]+"_noise"))

    grid_out = TextGrid
    
    
    outFile_TextGrid = noise_textgrid_dir + sentence_
    tgt.io.write_to_file(grid_out, outFile_TextGrid, format='long')
    return 1


for wav in wav_list:
    print('\n\n',wav)  

    SR, WavFile = scipy.io.wavfile.read(source_dir + wav)
    hop_length = 48 # 3 ms windows
    Pr_WavFile = python_speech_features.sigproc.preemphasis(WavFile, coeff=0.97)
    HighP_WavFile = butter_highpass_filter(Pr_WavFile, 200, 16000, order=5)
    noise_boundary = get_noise_boundary(SR, HighP_WavFile, hop_length)
    TextGrid_modified = create_new_textgrid(wav, noise_boundary)
    

    
