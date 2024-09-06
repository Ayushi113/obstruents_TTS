############
# This script extracts stops from all the contexts and puts them in a folder stops_with_closure.
# Functionality for specific contexts (CV, VC, VCV) has also been coded, but switched off.
#############
import tgt, os
import numpy as np
import sox, sys
System = sys.argv[1]
grid_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.textgrids_MFA/'
wav_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.wavs_16K/'


fricatives = ['F', 'V', 'S', 'SH', 'HH']
stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]

vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']


wavFiles = [wav for wav in os.listdir(wav_dir) if wav.endswith('.wav')]
gridFiles = [grid for grid in os.listdir(grid_dir) if grid.endswith('.TextGrid')]
for grid in gridFiles:
    #print(grid)
    textgrid = tgt.io.read_textgrid(grid_dir + grid)
    words_tier = textgrid.get_tier_by_name('sentence - words')
    phonemes_tier = textgrid.get_tier_by_name('sentence - phones')

    for idx_w, word in enumerate(words_tier):

        word_start = word.start_time
        word_end = word.end_time
        phone_seq = phonemes_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=False, right_overlap=False)
        #phones_label = [ph.text for ph in phone_seq]
        if any(ph.text in stops for ph in phone_seq):
           for idx_p, ph in enumerate(phone_seq):
               destination_dir = '../data/' + System + '/02.stops_with_closure/'
               #if idx_p == 0:
               #   destination_dir = destination_dir + 'CV_initial/'
               #elif idx_p == len(phone_seq)-1:
               #     destination_dir = destination_dir + 'VC_final/'
               #else:
               #    destination_dir = destination_dir + 'VCV_medial/'

               if ph.text in stops:
                  stop_start = ph.start_time
                  stop_end = ph.end_time
                  stop_dur = stop_end - stop_start
                  stop_dur = np.round(stop_dur, 3)

                  grid_out = tgt.TextGrid()

                  word_out = tgt.IntervalTier(0.0, stop_dur, 'sentence - words')
                  phones_out = tgt.IntervalTier(0.0, stop_dur, 'sentence - phones')

                  grid_out.add_tier(word_out)
                  grid_out.add_tier(phones_out)

                  word_out.add_annotation(tgt.Interval(0.0, stop_dur, word.text))
                  phones_out.add_annotation(tgt.Interval(0.0, stop_dur, ph.text))
                  
               # cutting up the sound file:

                  inFile_wav = wav_dir + grid.replace(".TextGrid", ".wav")
                  
                  tfm = sox.Transformer()
                  tfm.trim(stop_start, stop_start + stop_dur)
                  tfm.rate(16000)
                  
                  outFile_TextGrid = destination_dir + grid.replace(".TextGrid", "") + '_' + str(idx_w) + '_' + word.text + '_' + str(idx_p) + '_' + ph.text + '.TextGrid'
                  tgt.io.write_to_file(grid_out, outFile_TextGrid, format='long')
                  outFile_wav = outFile_TextGrid.replace(".TextGrid", ".wav")

                  tfm.build(inFile_wav, outFile_wav)


print("System", System, "stops extracted!")


