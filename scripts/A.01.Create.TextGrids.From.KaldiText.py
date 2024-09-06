##################################################################
# This script takes sentence-id and sentence-text from a single 
# text file. Creates blank TextGrids with a sentence-tier.
#
# This can be used as input to Montreal Forced Aligner.   					
##################################################################

import os, sys
import tgt
import librosa, string
# Change this every time
system = sys.argv[1]
# Get list of files without extension
audio_path = '../../Complete_Dataset/systems_to_montreal/' + system
print(audio_path)
if not os.path.isdir(audio_path):   
   print("No directory...")
   exit(0)


audio_list = [os.path.join(dp, f) for dp, dn, filenames in os.walk(audio_path) for f in filenames if os.path.splitext(f)[1] == '.wav'] # change to ".wav/.WAV" as per use
filenames = [os.path.splitext(os.path.basename(fil))[0] for fil in audio_list]
#punc_table = str.maketrans({key: None for key in string.punctuation})
  
# Get list of speaker IDs
text = '../text_data/A.01.Prompts.With.ID.txt'
text_fil = open(text).read().splitlines()
speaker_IDS = [[lin.split('\t')[0],lin.split('\t')[1].lower()]  for lin in text_fil]
#speaker_IDS = {item[0]:item[1].translate(punc_table) for item in speaker_IDS}
speaker_IDS = {item[0]:item[1] for item in speaker_IDS}
# Compare speaker IDs with Audio
for spk in filenames:

    for spkID, sent in speaker_IDS.items():
        spkID = spkID.strip()
        print(spkID, "speakerID\n\n")
        print(spk)
        if spk == spkID:
           print(spk)
           textgrid = tgt.TextGrid()
           start = 0.0
           duration = librosa.get_duration(filename=audio_path + '/' + spk + '.wav') # change to ".wav/.WAV" as per use
           sent_tier = tgt.IntervalTier(start, duration, 'sentence')
           sent_ann = speaker_IDS[spkID]
           print(sent_ann)
           sent_tier.add_annotation(tgt.Interval(start, duration, sent_ann))
           textgrid.add_tier(sent_tier)
           tgtName = audio_path + '/' + spk + '.TextGrid'
           print(tgtName, "hell")
           tgt.io.write_to_file(textgrid, tgtName, format='long', encoding='utf-8')


