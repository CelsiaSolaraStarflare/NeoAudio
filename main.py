# Import libraries
import random
import numpy as np
import librosa
import soundfile as sf

# Define parameters
sample_rate = 44100 # Hz
duration = 30 # seconds
notes = ["C", "D", "E", "F", "G", "A", "B"] # musical notes
octaves = [3, 4, 5] # octaves
frequencies = {"C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23, "G": 392.00, "A": 440.00, "B": 493.88} # frequencies in Hz
tempo = 120 # beats per minute
beat = 60 / tempo # seconds per beat

# Generate a random melody
melody = []
for i in range(int(duration / beat)):
    note = random.choice(notes) # choose a random note
    octave = random.choice(octaves) # choose a random octave
    frequency = frequencies[note] * (2 ** (octave - 4)) # calculate the frequency
    melody.append(frequency)

# Generate a sine wave for each note
wave = []
for frequency in melody:
    t = np.linspace(0, beat, int(beat * sample_rate), False) # time vector
    s = np.sin(frequency * t * 2 * np.pi) # sine wave
    wave.append(s)

# Concatenate the waves
wave = np.concatenate(wave)

# Add some noise to make it more realistic
noise = np.random.normal(0, 0.01, len(wave)) # Gaussian noise
wave = wave + noise

# Normalize the wave to [-1, 1]
wave = wave / np.max(np.abs(wave))

# Save the wave as a wav file
sf.write("song.wav", wave, sample_rate)
