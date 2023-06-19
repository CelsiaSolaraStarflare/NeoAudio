# Import libraries
import numpy as np
import librosa
import soundfile as sf

# Load the audio file
audio, sample_rate = librosa.load("song.wav")

# Calculate the loudness of the audio
loudness = librosa.feature.rms(audio)[0]

# Define a function to find the peaks of the loudness
def find_peaks(loudness):
    # Initialize an empty list for the peaks
    peaks = []
    # Initialize a counter for the index
    i = 0
    # Loop through the loudness array
    while i < len(loudness) - 1:
        # Compare the current loudness with the next loudness
        if loudness[i] > loudness[i+1]:
            # If the current loudness is greater than the next loudness, it is a peak
            peaks.append(i)
        # Increment the index by 1
        i += 1
    # Return the peaks list
    return peaks

# Find the peaks of the loudness
peaks = find_peaks(loudness)

# Define a function to extract a beat from the audio
def extract_beat(audio, peak, sample_rate):
    # Define a window size for the beat in seconds
    window_size = 0.5
    # Calculate the window size in samples
    window_size_samples = int(window_size * sample_rate)
    # Extract the audio segment around the peak
    beat = audio[peak - window_size_samples : peak + window_size_samples]
    # Return the beat array
    return beat

# Define a function to compare two beats
def compare_beats(beat1, beat2):
    # Return True if the beats are similar, False otherwise
    # Use a simple correlation coefficient as a measure of similarity
    return np.corrcoef(beat1, beat2)[0, 1] > 0.9

# Define a function to find the pattern of beats
def find_pattern(audio, peaks, sample_rate):
    # Initialize an empty list for the pattern
    pattern = []
    # Initialize an empty list for the beats
    beats = []
    # Loop through the peaks list
    for peak in peaks:
        # Extract a beat from the audio at each peak
        beat = extract_beat(audio, peak, sample_rate)
        # Append the beat to the beats list
        beats.append(beat)
        # Initialize a flag to indicate if the beat is repeated or not
        repeated = False
        # Loop through the previous beats in the beats list
        for i in range(len(beats) - 1):
            # Compare the current beat with each previous beat
            if compare_beats(beat, beats[i]):
                # If they are similar, append the index of the previous beat to the pattern and set the flag to True
                pattern.append(i)
                repeated = True
                break
        # If none of the previous beats are similar to the current beat, append -1 to the pattern and set the flag to False 
        if not repeated:
            pattern.append(-1)
    # Return the pattern list and the beats list 
    return pattern, beats

# Find the pattern of beats from the audio and peaks 
pattern, beats = find_pattern(audio, peaks, sample_rate)
