import os
from re import template
import librosa
import librosa.display
import numpy as np

from common import *


def mfcc_extract(sound, sr):
    mfcc = librosa.feature.mfcc(
        y=sound, n_mfcc=13, sr=sr, n_mels=128, fmax=8000, power=2, n_fft=1024
    )
    delta_mfcc = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)
    return np.concatenate((mfcc, delta_mfcc, delta2_mfcc))


def dtw(sound, reference):
    D, wp = librosa.sequence.dtw(sound, reference, subseq=True, metric="euclidean")
    return D[-1, -1] / wp.shape[0]


LABELS.remove("sil")
template_mfccs = {}

for label in LABELS:
    template_mfccs[label] = []
    for count in range(1, SAMPLE_COUNT + 1):
        file = f"{SAMPLE_DIR}/{label}-{count}.wav"
        sample, sample_sr = librosa.load(file)
        sample_mfcc = mfcc_extract(sample, sample_sr)
        template_mfccs[label].append(sample_mfcc)


def do_recognition(file: str) -> str:
    # load sample
    sample, sample_sr = librosa.load(file)
    sample_mfcc = mfcc_extract(sample, sample_sr)

    # calculate dtw distance from sample to all templates
    distances = {}
    for label in LABELS:
        distances[label] = []
        for template_mfcc in template_mfccs[label]:
            distances[label].append(dtw(sample_mfcc, template_mfcc))

    # find the shortest distance for each label
    min_distances = {}
    for label in LABELS:
        min_distances[label] = min(distances[label])

    # print(min_distances)

    # shortest distance is the match
    min_label = min(min_distances, key=min_distances.get)

    return min_label


for label in LABELS:
    correct_label = label
    recd = []

    for file in os.listdir(f"audio_per_labels/audio/{label}"):
        if file.endswith(".wav"):
            recd_label = do_recognition(f"audio_per_labels/audio/{label}/{file}")
            recd.append(recd_label)

    # calculate accuracy in percentage
    accuracy = sum([1 for label in recd if label == correct_label]) / len(recd) * 100

    # calculate distribution of labels
    distribution = {}
    for label in LABELS:
        distribution[label] = recd.count(label) / len(recd) * 100

    # sort distribution
    sorted_distribution = sorted(distribution.items(), key=lambda x: x[1])
    sorted_distribution.reverse()

    print(f"Label {correct_label}, Accuracy: {accuracy:.2f}%", end=", ")

    for label, percentage in sorted_distribution:
        print(f"{label}: {percentage:.2f}%", end=", ")

    print()
