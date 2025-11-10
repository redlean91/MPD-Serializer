# https://github.com/redlean91/MPD-Serializer
# MPD Serializer for Just Dance
# Serializer for Media Presentation Description files to Just Dance-like format

import os
from MPD import MPD

ADD_JD_URL = True

os.makedirs("toSerialize", exist_ok=True)
os.makedirs("serialized", exist_ok=True)

print("Media Presentation Description Serializer for Just Dance\nhttps://github.com/redlean91/MPD-Serializer\n")

for file in os.listdir("toSerialize"):
    if not file.endswith(".mpd"): 
        print(f"[{file}]: Not a valid MPD file!")
        continue
    else:
        print(f"[{file}] Serializing...")
        with open(os.path.join("serialized", f"{file}.ckd"), "wb") as f:
            inst = MPD(mpd_path=os.path.join("toSerialize", file), fileStream=f, add_jd_url=ADD_JD_URL)
            inst.Serialize()
        print(f"[{file}] Serialized!")