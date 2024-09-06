#!/bin/sh
start=$SECONDS 
#Usage: bash extract_basic_feats.sh A

python3 ./C.01.Extract.Stops.From.MFA.py $1 || exit 1
python3 ./C.02.Create.Empty.Noise.Tiers.py $1 || exit 1
python3 ./C.03.Mark.Noise.Boundaries.CV.py $1 || exit 1
python3 ./C.04.Extract.Stops.Noise.From.MFA.py $1 || exit 1
python3 ./C.05.Extract.Fricatives.From.MFA.py $1 || exit 1
python3 ./C.06.Separate.Consonants.Into.Contexts.py $1 || exit 1
python3 ./C.07.Rearrange.Stops.Affricates.py $1 || exit 1
python3 ./C.08.Separate.Noise.Region.Context.py $1 || exit 1
python3 ./V.01.Extract.Vowels.From.MFA.py $1 || exit 1
python3 ./C.09.Extract.Duration.py $1 CV || exit 1 # remember TWO arguments
python3 ./C.09.Extract.Duration.py $1 VC || exit 1 # remember TWO arguments
python3 ./C.09.Extract.Duration.py $1 isolate || exit 1 # remember TWO arguments
python3 ./C.10.Extract.Amplitude.py $1 CV || exit 1 # remember TWO arguments
python3 ./C.10.Extract.Amplitude.py $1 VC|| exit 1 # remember TWO arguments
python3 ./C.10.Extract.Amplitude.py $1 isolate || exit 1 # remember TWO arguments
python3 ./C.11.Extract.Spectrals.py $1 CV || exit 1 # remember TWO arguments
python3 ./C.11.Extract.Spectrals.py $1 VC || exit 1 # remember TWO arguments
python3 ./C.11.Extract.Spectrals.py $1 isolate || exit 1 # remember TWO arguments
python3 ./C.12.Add.Columns.Phon.Descriptors.Contextual.py $1 CV || exit 1 # remember TWO arguments
python3 ./C.12.Add.Columns.Phon.Descriptors.Contextual.py $1 VC || exit 1 # remember TWO arguments
python3 ./C.12.Add.Columns.Phon.Descriptors.Contextual.py $1 isolate || exit 1 # remember TWO arguments
python3 ./V.02.Extract.Duration.py $1 || exit 1 # only ONE argument.
python3 ./V.03.Extract.Amplitude.py $1 || exit 1 # only ONE argument.
python3 ./V.04.Extract.Spectrals.py $1 || exit 1 # only ONE argument. 
#python3 ./V.06.Formants.Wrapper.py $1 || exit 1
#python3 ./V.08.Variance.Wrapper.py $1 || exit 1
python3 ./V.09.Get.Minimum.Variance.py $1 || exit 1
python3 ./V.10.Create.Optimized.Formants.File.py $1 || exit 1
python3 ./V.11.Get.Word.Label.py $1 || exit 1
Rscript ./V.12.Separate.Lower.Higher.Formants.R $1 || exit 1
python3 ./V.13.Add.Columns.Phon.Descriptors.py $1 || exit 1
python3 ./V.14.Calculate.Relative.Amplitude.py $1 CV || exit 1
python3 ./V.14.Calculate.Relative.Amplitude.py $1 VC || exit 1

Rscript ./A.04.Generate.Merged.Files.R $1 || exit 1
python3 ./C.13.Consonant.Dunn.Contextual.ipynb || exit 1
duration=$(( SECONDS - start ))
echo $duration
echo $duration $"is how long it took!"
