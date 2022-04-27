# creates mfcc features for a given audio file

from audioop import mul
import librosa
import librosa.display
import os, shutil
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

from common import *


def extract_mfcc(folder: str, file: str) -> np.ndarray:
    y, sr = librosa.load(f"audio_per_labels/audio/{folder}/{file}.wav")
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    mfcc = librosa.feature.mfcc(S=S, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    return np.concatenate((mfcc, mfcc_delta, mfcc_delta2))


def extract_mfccs(folder):
    os.mkdir(f"mfcc/{folder}")
    os.mkdir(f"mfcc/{folder}/npy")
    os.mkdir(f"mfcc/{folder}/plt")
    for file in os.listdir(f"audio_per_labels/audio/{folder}"):
        if file.endswith(".wav"):
            ret = extract_mfcc(folder, file)


try:
    shutil.rmtree("mfcc")
except FileNotFoundError:
    pass

os.mkdir("mfcc")

print(extract_mfcc("A", "1_10"))
