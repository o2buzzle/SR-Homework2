# Read through labels and remove Audacity's annoying frequency markers
import os

files = os.listdir("data/labels")
for file in files:
    with open(f"data/labels/{file}", "r") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if line[0] == "\\":
            continue
        new_lines.append(line)
    with open(f"data/labels.new/{file}", "w") as f:
        f.writelines(new_lines)
