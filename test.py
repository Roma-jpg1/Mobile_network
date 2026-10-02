import numpy as np
import sounddevice as sd


FS = 44_100          
TOTAL_TIME = 15.0    
BPM = 130             
BEAT = 60 / BPM



NOTES = {
    "си3": 246.94,
    "до#4": 277.18,
    "ре#4": 311.13,
    "ми4": 329.63,
    "фа#4": 369.99,
    "соль#4": 415.30,
    "ля4": 440.00,
    "си4": 493.88,
    "до#5": 554.37,
}


MELODY = [
    # I'm a Barbie girl
    ("соль#4", 0.5),
    ("ми4", 0.5),
    ("соль#4", 0.5),
    ("до#5", 0.5),
    ("ля4", 2.0),

    # In the Barbie world
    ("фа#4", 0.5),
    ("ре#4", 0.5),
    ("фа#4", 0.5),
    ("си4", 0.5),
    ("соль#4", 1.0),
    ("фа#4", 0.5),
    ("ми4", 1.0),
    ("до#4", 2.0),

    # Life in plastic
    ("ми4", 0.5),
    ("до#4", 0.5),
    ("фа#4", 2.0),
    ("до#4", 1.0),
    ("си3", 2.0),

    # It's fantastic
    ("фа#4", 0.5),
    ("ми4", 0.5),
    ("соль#4", 2.0),
    ("си4", 1.0),
    ("фа#4", 2.0),
]

target_samples = int(FS * TOTAL_TIME)
signal = []
current_samples = 0

while current_samples < target_samples:
    for note_name, beats in MELODY:
        samples = int(FS * beats * BEAT)
        time = np.arange(samples) / FS
        note = np.sin(2 * np.pi * NOTES[note_name] * time)
        signal.append(note)
        current_samples += samples

        if current_samples >= target_samples:
            break

audio = np.concatenate(signal)
sd.play(audio, FS)
sd.wait()
