# creates mfcc features for a given audio file

from audioop import mul
import librosa
import librosa.display
import os, shutil
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

from common import *


def extract_mfcc_label(folder):
    os.mkdir(f"mfcc/{folder}")
    os.mkdir(f"mfcc/{folder}/npy")
    os.mkdir(f"mfcc/{folder}/plt")
    for file in os.listdir(f"audio_per_labels/audio/{folder}"):
        if file.endswith(".wav"):
            y, sr = librosa.load(f"audio_per_labels/audio/{folder}/{file}")
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
            mfccs = librosa.feature.mfcc(S=S, n_mfcc=39)
            fig, ax = plt.subplots(nrows=2, sharex=True)
            img = librosa.display.specshow(
                librosa.power_to_db(S, ref=np.max),
                x_axis="time",
                y_axis="mel",
                fmax=8000,
                ax=ax[0],
            )
            fig.colorbar(img, ax=[ax[0]])
            ax[0].set(title="Mel spectrogram")
            ax[0].label_outer()
            img = librosa.display.specshow(mfccs, x_axis="time", ax=ax[1])
            fig.colorbar(img, ax=[ax[1]])
            ax[1].set(title="MFCC")

            # Save the NumPy array and the plot
            np.save(f"mfcc/{folder}/npy/{file[:-4]}", mfccs)
            plt.savefig(f"mfcc/{folder}/plt/{file[:-4]}")
            plt.close()


try:
    shutil.rmtree("mfcc")
except FileNotFoundError:
    pass

os.mkdir("mfcc")

with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    pool.map(extract_mfcc_label, os.listdir("audio_per_labels/audio"))
