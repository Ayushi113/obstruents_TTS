############################################################################################################################ 
#Composer: Ayushi Pandey, 2019  
#Credits: Colin Wilson's old script, and adding features from ChrisDicanio and Mietta Lanes (https://depts.washington.edu/phonlab/resources/f0-F1-F2-intensity_praat_script.praat)
#Functions: 
# --- Vowel formants -- onset, offset and midpoint. 
# --- Amplitude values at onset, offset, midpoint.
# --- Runs over a directory
############################################################################################################################

form Enter ceiling values
     comment Please enter the ceiling value:
     real formant_ceiling 
     word sys_name 
endform
ceiling$ = string$(formant_ceiling)
writeInfoLine: "System name is:-", sys_name$
appendInfoLine: "Ceiling value is:-", formant_ceiling
wavdir$ = "../../Complete_Dataset/output_montreal/" + sys_name$ + "/01.wavs_16K"  
griddir$ = "../../Complete_Dataset/output_montreal/" + sys_name$ + "/01.textgrids_MFA"
resultsfile$ = "../data/" + sys_name$ + "/08.formants_and_variances/Results-" + ceiling$ + ".txt"

tier = 2
formant_step = 0.0010

# Make a listing of all the sound files in a directory:
Create Strings as file list... list 'wavdir$'/*.wav
numberOfFiles = Get number of strings

# Create a header row:
header$ = "Filename	TextGridLabel	Duration	F0_onset	F1_onset	F2_onset	F3_onset	F3_band_onset	F4_onset	F5_onset	F5_band_onset	F1_midpoint	F2_midpoint	F3_midpoint	F3_band_midpoint	F4_midpoint	F5_midpoint	F5_band_midpoint	F0_offset	F1_offset	F2_offset	F3_offset	F3_band_offset	F4_offset	F5_offset	F5_band_offset'newline$'"
fileappend "'resultsfile$'" 'header$'


# Open each sound file in the directory:
for ifile to numberOfFiles
	filename$ = Get string... ifile
	writeInfoLine: filename$ 
	Read from file... 'wavdir$'/'filename$'

	# get the name of the sound object:
	soundname$ = selected$ ("Sound", 1)
	appendInfoLine: soundname$	

	# Look for a TextGrid by the same name:
	gridfile$ = griddir$ + "/" + soundname$ +  ".TextGrid"
	appendInfoLine: gridfile$

	# if a TextGrid exists, open it and do the analysis:
	if fileReadable (gridfile$)
		Read from file... 'gridfile$'

		select Sound 'soundname$'
		To Formant (burg)... 0 6 formant_ceiling 0.025 50
		
		select TextGrid 'soundname$'
		numberOfIntervals = Get number of intervals... tier
		appendInfoLine: numberOfIntervals


		# Pass through all intervals in the designated tier, and if they have a label, do the analysis:
		for interval to numberOfIntervals
			label$ = Get label of interval... tier interval
			appendInfoLine: label$
			if index_regex(label$, "(AA0|AA1|AA2|AE0|AE1|AE2|AH0|AH1|AH2|AO0|AO1|AO2|AW0|AW1|AW2|AY0|AY1|AY2|EH0|EH1|EH2|ER0|ER1|ER2|EY0|EY1|EY2|IH0|IH1|IH2|IY0|IY1|IY2|OW0|OW1|OW2|OY0|OY1|OY2|UH0|UH1|UH2|UW0|UW1|UW2)")
				# duration:
				start = Get starting point... tier interval
				end = Get end point... tier interval
				duration = end-start
				midpoint = (start + end) / 2
				onset = start+(duration/5)
				offset = end-(duration/5)
				appendInfoLine: "Vowel duration:", duration


				# formants:
				select Formant 'soundname$'
				
				
				# TAKE FORMANT MEASUREMENTS
				#f0_on = Get pitch
				f1_on = Get value at time... 1 onset Hertz Linear
				f2_on = Get value at time... 2 onset Hertz Linear
				f3_on = Get value at time... 3 onset Hertz Linear
                                f4_on = Get value at time... 4 onset Hertz Linear
				f5_on = Get value at time... 5 onset Hertz Linear
				appendInfoLine: "onset formants", f1_on, f2_on, f5_on
				
                               f3_band_on = Get bandwidth at time... 3 onset Hertz Linear
			       f5_band_on = Get bandwidth at time... 5 onset Hertz Linear
                               appendInfoLine: "onset bandwidth F3 and F5", f3_band_on, f5_band_on
				

				f1_mid = Get value at time... 1 midpoint Hertz Linear
				f2_mid = Get value at time... 2 midpoint Hertz Linear
				f3_mid = Get value at time... 3 midpoint Hertz Linear
                                f4_mid = Get value at time... 4 midpoint Hertz Linear
				f5_mid = Get value at time... 5 midpoint Hertz Linear
								
                                f3_band_mid = Get bandwidth at time... 3 midpoint Hertz Linear
				f5_band_mid = Get bandwidth at time... 5 midpoint Hertz Linear
                               appendInfoLine: "onset bandwidth F3 and F5", f3_band_mid, f5_band_mid


				f1_off = Get value at time... 1 offset Hertz Linear
				f2_off = Get value at time... 2 offset Hertz Linear
				f3_off = Get value at time... 3 offset Hertz Linear
                                f4_off = Get value at time... 4 offset Hertz Linear
				f5_off = Get value at time... 5 offset Hertz Linear
				
                                f3_band_off = Get bandwidth at time... 3 offset Hertz Linear
				f5_band_off = Get bandwidth at time... 5 offset Hertz Linear
                                appendInfoLine: "onset bandwidth F3 and F5", f3_band_off, f5_band_off
				
				# pitch - values taken from this paper - https://bit.ly/2XBFIEZ 
				select Sound 'soundname$'
				To Pitch... 0.01 70 500
				
				appendInfoLine: "Here pitch"
				select Pitch 'soundname$'
				pitch = selected("Pitch")
                              pitch_on = Get maximum... start onset Hertz Parabolic
                              appendInfoLine: pitch_on, "onset"
				
                             if pitch_on = undefined
				   onset = onset + 'formant_step'
				   start = start + 'formant_step'
				   select Pitch 'soundname$'
				   pitch_on = Get maximum... start onset Hertz Parabolic
                                appendInfoLine: "pitch after correction onset", pitch_on

				endif
				
                             pitch_off = Get maximum... offset end Hertz Parabolic
                             appendInfoLine: pitch_off, "offset"

				if pitch_off = undefined			   
				   offset = offset - 'formant_step'
				   end = end - 'formant_step'
				   select Pitch 'soundname$'
				   pitch_off = Get maximum... offset end Hertz Parabolic
                                appendInfoLine: "pitch after correction offset", pitch_off
                            endif

                            select TextGrid 'soundname$'
				# Save result to text file:
         		    resultline$ = "'soundname$'	'label$'	'duration'	'pitch_on'	'f1_on'	'f2_on'	'f3_on'	'f3_band_on'	'f4_on'	'f5_on'	'f5_band_on'	'f1_mid'	'f2_mid'	'f3_mid'	'f3_band_mid'	'f4_mid'	'f5_mid'	'f5_band_mid'	'pitch_off'	'f1_off'	'f2_off'	'f3_off'	'f3_band_off'	'f4_off'	'f5_off'	'f3_band_off''newline$'"
                            fileappend "'resultsfile$'"  'resultline$'

           else
				# duration:
				start = Get starting point... tier interval
				end = Get end point... tier interval
				duration = end-start
				appendInfoLine: "Consonant duration:", duration
						
				# select the TextGrid so we can iterate to the next interval:
				select TextGrid 'soundname$'
				# Save result to text file:
				resultline$ = "'soundname$'	'label$'	'duration' 'newline$'"
                              fileappend "'resultsfile$'" 'resultline$'
              endif
		endfor
		# Remove the TextGrid, Formant, and Pitch objects
		select TextGrid 'soundname$'
		plus Formant 'soundname$'
		plus Pitch 'soundname$'
		Remove
	endif
	# Remove the Sound object
	select Sound 'soundname$'
	Remove
	# and go on with the next sound file!
	select Strings list
endfor

# When everything is done, remove the list of sound file paths:
Remove

