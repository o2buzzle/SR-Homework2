# Randomly select a set of template data from a given dataset

import random
import os
import shutil

from common import *

random_os = random.SystemRandom()

LABELS.remove("sil")
try:
    shutil.rmtree("sample_data")
except FileNotFoundError:
    pass

os.mkdir("sample_data")

for label in LABELS:
    for count in range(1, SAMPLE_COUNT + 1):
        files = os.listdir(f"audio_per_labels/audio/{label}")
        files = [file for file in files if file.endswith(".wav")]
        random_os.shuffle(files)
        for file in files[:SAMPLE_COUNT]:
            shutil.copy(
                f"audio_per_labels/audio/{label}/{file}",
                f"sample_data/{label}-{count}.wav",
            )
