## SR-Homework2: Isolated Word Speech Recognition

# Within `src/` is a full "toolchain" for performing speech recognition

```
label_fixer.py - Prepare labels to the correct format
sound_segmenter.py - Segment audio files using Audacity's simple label format
mfcc.py - MFCCs extraction from audio files
dtw.py - Simple naive implementation of the DTW algorithm for speech recognition
GMM-HMM.ipynb - Simple implementation of a GMMHMM model for speech recognition
```

To run:
- Clone the repository
- Install requirements - `pip install -r requirements.txt`
- Put audio and label data into `data/`
- (Optional) Fix labels if they are in the extended format 
- Segment the audio data (`sound_segmenter.py`)
- Run the algorithms

Demo:

![Demo](https://github.com/o2buzzle/SR-Homework2/raw/main/media/demo.gif)
