import os
import pydub
import shutil

shutil.rmtree("output")
os.mkdir("output")
os.mkdir("output/audio")

LABELS = ["len", "xuong", "trai", "phai", "nhay", "ban", "A", "B", "sil"]
for label in LABELS:
    os.mkdir(f"output/audio/{label}")


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
            start, stop, label = line.split("\t")
            labels.append(SoundSegment(float(start), float(stop), label.strip()))

    # chop each label into its own wav
    for order, label in enumerate(labels):
        audio = pydub.AudioSegment.from_wav(f"data/audio/{file}.wav")
        audio = audio[int(label.start * 1000) : int(label.end * 1000)]
        audio.export(f"output/audio/{label.label}/{file}_{order+1}.wav", format="wav")
