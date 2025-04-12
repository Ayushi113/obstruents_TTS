# Production Characteristics of Obstruents in WaveNet and Older TTS Systems  
**Ayushi Pandey, Sébastien Le Maguer, Julie Carson-Berndsen, Naomi Harte**  
📚 _Proc. Interspeech 2022, pp. 2373–2377_  
📌 DOI: [10.21437/Interspeech.2022-10606](https://doi.org/10.21437/Interspeech.2022-10606)

---

## Overview

This repository outlines the complete processing and feature extraction pipeline used in our Interspeech 2022 paper:  
> **Production Characteristics of Obstruents in WaveNet and Older TTS Systems**  

We analyze obstruents across 14 TTS systems (including WaveNet and older ones) using forced alignment and contextual feature extraction.

---

## 📁 Directory Setup

```bash
WD=/home/ayushi/Projects_2020/Naturalness  # Set your working directory
```

- Raw dataset: `Complete_Dataset/Raw.Data`
- Transcripts: `raw_blizzard_data/raw.Bliz.data.txt`

---

## 🔄 Preprocessing Pipeline

### 1. Prepare Dataset
```bash
cd $WD/Complete_Dataset/Raw.Data
```

Rearrange wave files system-wise:
```bash
mkdir $WD/Complete_Dataset/systems_to_montreal/{A..Z}
cp $WD/Complete_Dataset/Raw.Data/A/*.wav $WD/Complete_Dataset/systems_to_montreal/A/
```

Assign sentence IDs:
```bash
cd $WD/Complete_Dataset/systems_to_montreal/A
ls *.wav | sed 's/.wav//g' > Name.of.Files.txt
cp ../../raw_blizzard_data/raw.Bliz.data.txt .
paste Name.of.Files.txt raw.Bliz.data.txt > 01.Prompts.With.ID.txt
cp 01.Prompts.With.ID.txt $WD/organized_InterSpeech_2022/02.text_data/
```

---

## 🎯 Forced Alignment

### 2. Create TextGrids using Kaldi transcripts
```bash
cd $WD/organized_InterSpeech_2022/scripts
python3 A.01.Create.TextGrids.From.KaldiText.py A
```

### 3. Create Variant-Free Lexicon

```bash
cd /home/ayushi/Tools/montreal-forced-aligner_linux/montreal-forced-aligner
bin/mfa_align $WD/Complete_Dataset/systems_to_montreal/A \
              $WD/organized_InterSpeech_2022/text_data/02.Librispeech.Lexicon.Lower.txt \
              english \
              $WD/Complete_Dataset/output_montreal_1stpass/A_1stpass

cd $WD/organized_InterSpeech_2022/scripts
python3 A.02.Get.Montreal.Choice.for.NatBliz.py
```

Use the variant-free lexicon for final alignment:
```bash
bin/mfa_align $WD/Complete_Dataset/systems_to_montreal/A \
              $WD/organized_InterSpeech_2022/text_data/03.Blizzard.Lexicon.No.Variation.txt \
              english \
              $WD/Complete_Dataset/output_montreal/A
```

---

## 🔉 Downsampling

```bash
cd $WD/Complete_Dataset/raw_blizzard_data/A
for i in *wav; do sox $i -r 16k ${i}_16k.wav; done

mkdir $WD/Complete_Dataset/output_montreal/A/01.wavs_16K
mv ./*.wav_16k.wav $WD/Complete_Dataset/output_montreal/A/01.wavs_16K

cd $WD/Complete_Dataset/output_montreal/A/01.wavs_16K
rename 's/\.wav_16k.wav$/.wav/' *.wav_16k.wav
```

---

## 📂 Data Organization

Prepare directories for storing intermediate results:
```bash
cd $WD/organized_InterSpeech_2022/data
for dir in */; do mkdir -p "$dir"/{02.stops_with_closure,03.textgrids_noise,...}; done
```

---

## 🧠 Feature Extraction Scripts

### Obstruents (Consonants)

```bash
python3 C.01.Extract.Stops.From.MFA.py A
python3 C.05.Extract.Fricatives.From.MFA.py A
python3 C.06.Separate.Consonants.Into.Contexts.py A
python3 C.09.Extract.Duration.py A CV
python3 C.10.Extract.Amplitude.py A CV
python3 C.11.Extract.Spectrals.py A CV
```

### Vowels

```bash
python3 V.01.Extract.Vowels.From.MFA.py A
python3 V.02.Extract.Duration.py A
python3 V.03.Extract.Amplitude.py A
python3 V.04.Extract.Spectrals.py A
python3 V.06.Formants.Wrapper.py
python3 V.08.Variance.Wrapper.py
python3 V.09.Get.Minimum.Variance.py
python3 V.10.Create.Optimized.Formants.File.py
python3 V.11.Get.Word.Label.py
Rscript V.12.Separate.Lower.Higher.Formants.R A
python3 V.13.Add.Columns.Phon.Descriptors.py
python3 V.14.Calculate.Relative.Amplitude_CV.py
python3 V.14.Calculate.Relative.Amplitude_VC.py
```

---

## 📊 Final Merge

```bash
python3 A.03.Ind2Mega.Combine.Features.py
```

---

## 📌 Citation

If you use this work, please cite:

```bibtex
@inproceedings{Pandey2022ProductionCO,
  title     = {{Production characteristics of obstruents in WaveNet and older TTS systems}},
  author    = {Ayushi Pandey and S{'e}bastien Le Maguer and Julie Carson-Berndsen and Naomi Harte},
  year      = {2022},
  booktitle = {Proc. Interspeech 2022},
  pages     = {2373--2377},
  doi       = {10.21437/Interspeech.2022-10606},
}
```
