import tgt, os
import sys
System = sys.argv[1]

source_dir = '../../Complete_Dataset/output_montreal/' + System + '/01.textgrids_MFA/'
destination_dir = '../data/' + System + '/03.textgrids_noise/'

for grid in os.listdir(source_dir):
	TextGrid = tgt.io.read_textgrid(source_dir + grid)
	TG_start = TextGrid.start_time
	TG_end = TextGrid.end_time
	noise_out = tgt.IntervalTier(0.0, TG_end, 'sentence - noise')
	TextGrid.add_tier(noise_out)
	outFile_TextGrid = destination_dir + grid.replace(".TextGrid", "_noise.TextGrid")
	tgt.io.write_to_file(TextGrid, outFile_TextGrid, format='long')
