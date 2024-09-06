import tgt, os, sys
import numpy as np
import sox
System = sys.argv[1]

grid_dir = '../data/' + System + '/03.textgrids_noise/'
wav_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.wavs_16K/'


stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]

vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']


wavFiles = [wav for wav in os.listdir(wav_dir) if wav.endswith('.wav')]
gridFiles = [grid for grid in os.listdir(grid_dir) if grid.endswith('.TextGrid')]
for grid in gridFiles:
    print(grid)
    textgrid = tgt.io.read_textgrid(grid_dir + grid)
    words_tier = textgrid.get_tier_by_name('sentence - words')
    phones_tier = textgrid.get_tier_by_name('sentence - phones')
    noise_tier = textgrid.get_tier_by_name('sentence - noise')


    for idx_w, word in enumerate(words_tier):

        word_start = word.start_time
        word_end = word.end_time
        phone_seq = phones_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=False, right_overlap=False)
        obstruent_indices = [ph_idx for ph_idx, ph in enumerate(phone_seq) if ph.text in stops]
        noise_phone_seq = noise_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=False, right_overlap=False)
        
        if noise_phone_seq != []:
           noise_indices = [ns_idx for ns_idx, ns_reg in enumerate(noise_phone_seq)]
           correspondence_noise_id = {noise_indices[i]: obstruent_indices[i] for i in range(len(noise_indices))}
        #print(word.text, obstruent_indices, noise_phone_seq, len(obstruent_indices), len(noise_phone_seq)) 
        #phones_label = [ph.text for ph in phone_seq]
        if any(ph.text.split('.')[0] in stops for ph in noise_phone_seq):
           for idx_p, ph_noise in enumerate(noise_phone_seq):
               destination_dir = '../data/' + System + '/04.noise_region_stops/'
               
               if ph_noise.text.split('.')[0] in stops:
                  stop_start = ph_noise.start_time
                  stop_end = ph_noise.end_time
                  stop_dur = stop_end - stop_start
                  stop_dur = np.round(stop_dur, 3)

                  grid_out = tgt.TextGrid()

                  word_out = tgt.IntervalTier(0.0, stop_dur, 'sentence - words')
                  noise_phones_out = tgt.IntervalTier(0.0, stop_dur, 'sentence - noise')

                  grid_out.add_tier(word_out)
                  grid_out.add_tier(noise_phones_out)

                  word_out.add_annotation(tgt.Interval(0.0, stop_dur, word.text))
                  noise_phones_out.add_annotation(tgt.Interval(0.0, stop_dur, ph_noise.text))
                  
               # cutting up the sound file:

                  inFile_wav = wav_dir + grid.replace("_noise.TextGrid", ".wav")
                  tfm = sox.Transformer()
                  tfm.trim(stop_start, stop_start + stop_dur)
                  tfm.rate(16000)
                  
                  outFile_TextGrid = destination_dir + grid.replace("_noise.TextGrid", "") + '_' + str(idx_w) + '_' + word.text + '_' + str(correspondence_noise_id[idx_p]) + '_' + ph_noise.text.split(".")[0] + '.TextGrid'
                  tgt.io.write_to_file(grid_out, outFile_TextGrid, format='long')
                  outFile_wav = outFile_TextGrid.replace(".TextGrid", ".wav")
                  tfm.build(inFile_wav, outFile_wav)





