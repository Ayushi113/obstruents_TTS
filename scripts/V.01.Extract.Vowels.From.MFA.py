import tgt, os, sys
import numpy as np
import sox
System = sys.argv[1]
grid_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.textgrids_MFA/'
wav_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.wavs_16K/'

fricatives =  ['F', 'V', 'S', 'Z', 'SH', 'ZH', 'DH', 'TH', 'HH']
stops = ["P", "B", "T", "D", "K", "G", "CH", "JH"]
obstruents = fricatives + stops
vowels = ['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2']


wavFiles = [wav for wav in os.listdir(wav_dir) if wav.endswith('.wav')]
gridFiles = [grid for grid in os.listdir(grid_dir) if grid.endswith('.TextGrid')]
CV_tokens = 0
VC_tokens = 0
CVC_tokens = 0

def vowel_output(phone):
    print(destination_dir)
    vowel_start = ph.start_time
    vowel_end = ph.end_time
    vowel_dur = vowel_end - vowel_start
    vowel_dur = np.round(vowel_dur, 3)

    grid_out = tgt.TextGrid()

    word_out = tgt.IntervalTier(0.0, vowel_dur, 'sentence - words')
    phones_out = tgt.IntervalTier(0.0, vowel_dur, 'sentence - phones')

    grid_out.add_tier(word_out)
    grid_out.add_tier(phones_out)

    word_out.add_annotation(tgt.Interval(0.0, vowel_dur, word.text))
    phones_out.add_annotation(tgt.Interval(0.0, vowel_dur, ph.text))
                  
               # cutting up the sound file:

    inFile_wav = wav_dir + grid.replace(".TextGrid", ".wav")
                  
    tfm = sox.Transformer()
    tfm.trim(vowel_start, vowel_start + vowel_dur)
    tfm.rate(16000)
                  
    outFile_TextGrid = destination_dir + grid.replace(".TextGrid", "") + '_' + obstruent + '_' + str(idx_w) + '_' + word.text + '_' + str(idx_p) + '_' + ph.text + '.TextGrid'
    tgt.io.write_to_file(grid_out, outFile_TextGrid, format='long')
    outFile_wav = outFile_TextGrid.replace(".TextGrid", ".wav")

    tfm.build(inFile_wav, outFile_wav)
    print("Written!")
    return(1)


for grid in gridFiles:
    print(grid)
    textgrid = tgt.io.read_textgrid(grid_dir + grid)
    words_tier = textgrid.get_tier_by_name('sentence - words')
    phonemes_tier = textgrid.get_tier_by_name('sentence - phones')

    for idx_w, word in enumerate(words_tier):
        print([word.text for word in words_tier])
        print(word)
        word_start = word.start_time
        word_end = word.end_time
        phone_seq = phonemes_tier.get_annotations_between_timepoints(word_start, word_end, left_overlap=False, right_overlap=False)

        for idx_p, ph in enumerate(phone_seq):
            destination_dir = ''              
            if ph.text in vowels and len(phone_seq) == 2: ## don't consider 1-length words
               if idx_p == 0 and phone_seq[idx_p+1].text in obstruents: ## words like "it"
                  print("Pure VC sequence -- initial")
                  VC_tokens = VC_tokens + 1
                  destination_dir = '../data/' + System + '/07.vowels/V1_VC/'
                  obstruent = phone_seq[idx_p+1].text
                  x_vc_inl = vowel_output(ph)

               elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1].text in obstruents:
                    print("Pure CV sequence -- final")
                    CV_tokens = CV_tokens + 1
                    destination_dir = '../data/' + System + '/07.vowels/V2_CV/'
                    obstruent = phone_seq[idx_p-1].text
                    x_cv_fnl = vowel_output(ph)

            elif ph.text in vowels and len(phone_seq) > 2: ## words like "can", "cats"
                 if idx_p == 0 and phone_seq[idx_p+1].text in obstruents: ## words like "it"
                    print("Pure VC sequence -- initial")
                    VC_tokens = VC_tokens + 1
                    destination_dir = '../data/' + System + '/07.vowels/V1_VC/'
                    obstruent = phone_seq[idx_p+1].text
                    x_vc_inl = vowel_output(ph)

                 elif idx_p == len(phone_seq)-1 and phone_seq[idx_p-1].text in obstruents:
                      print("Pure CV sequence -- final")
                      CV_tokens = CV_tokens + 1
                      destination_dir = '../data/' + System + '/07.vowels/V2_CV/'
                      obstruent = phone_seq[idx_p-1].text
                      x_cv_fnl = vowel_output(ph)

                 elif idx_p < len(phone_seq)-1:
                      if phone_seq[idx_p-1].text in obstruents and phone_seq[idx_p+1].text not in obstruents: # think "can"
                         if idx_p-1 == -1:
                            continue
                         else:
                            print("Pure CV sequence -- medial")
                            CV_tokens = CV_tokens + 1
                            destination_dir = '../data/' + System + '/07.vowels/V2_CV/'
                            obstruent = phone_seq[idx_p-1].text
                            x_cv_mdl = vowel_output(ph)

                      elif phone_seq[idx_p-1].text in obstruents and phone_seq[idx_p+1].text in obstruents: # think "cat"
                           print("CVC sequence -- medial")
                           CVC_tokens = CVC_tokens + 1
                           destination_dir = '../data/' + System + '/07.vowels/V2_CV/'
                           obstruent = phone_seq[idx_p-1].text
                           x_cv_mdl = vowel_output(ph)

                           destination_dir = '../data/' + System + '/07.vowels/V1_VC/'
                           obstruent = phone_seq[idx_p+1].text
                           x_vc_mdl = vowel_output(ph)

                      elif phone_seq[idx_p-1].text not in obstruents and phone_seq[idx_p+1].text in obstruents:
                           print("Pure VC sequence -- medial")
                           VC_tokens = VC_tokens + 1
                           destination_dir = '../data/' + System + '/07.vowels/V1_VC/'
                           obstruent = phone_seq[idx_p+1].text
                           x_cv_mdl = vowel_output(ph)

            else:
                print("Not a vowel!")


print("Number of CV", CV_tokens)
print("Number of CVC", CVC_tokens)
print("Number of VC", VC_tokens)


