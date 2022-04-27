import os
import pydub
import shutil

from common import *

try:
    shutil.rmtree("audio_per_labels")
except FileNotFoundError:
    pass


os.mkdir("audio_per_labels")
os.mkdir("audio_per_labels/audio")

for label in LABELS:
    os.mkdir(f"audio_per_labels/audio/{label}")


class SoundSegment:
    def __init__(self, start: float, end: float, label: str):
        self.start = start
        self.end = end
        self.label = label

    def __str__(self):
        return "({} - {}: {})".format(self.start, self.end, self.label)

    def __repr__(self):
        return self.__str__()


files = os.listdir("data/audio")
file_names = [file[:-4] for file in files]

# print(file_names)
for file in file_names:
    # read labels for that file
    labels = []
    with open(f"data/labels/{file}.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                continue
            start, stop, label = line.split("\t")
            labels.append(SoundSegment(float(start), float(stop), label.strip()))

    # chop each label into its own wav
    for order, label in enumerate(labels):
        audio = pydub.AudioSegment.from_wav(f"data/audio/{file}.wav")
        audio = audio[int(label.start * 1000) : int(label.end * 1000)]
        audio.export(
            f"audio_per_labels/audio/{label.label}/{file}_{order+1}.wav", format="wav"
        )
