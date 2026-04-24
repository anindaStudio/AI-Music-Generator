from midiutil import MIDIFile
import random
import os

# Create MIDI with 3 tracks
MyMIDI = MIDIFile(3)

# User input
mood = input("Enter mood (happy/sad/chill/energetic/romantic): ")
instrument = input("Choose instrument (piano/guitar/flute): ")

# Mood settings
if mood == "happy":
    tempo = 140
    scale = [60, 62, 64, 65, 67, 69, 71]
elif mood == "sad":
    tempo = 80
    scale = [60, 62, 63, 65, 67, 68, 70]
elif mood == "chill":
    tempo = 90
    scale = [60, 62, 65, 67, 69]
elif mood == "energetic":
    tempo = 160
    scale = [60, 64, 67, 72]
elif mood == "romantic":
    tempo = 70
    scale = [60, 63, 65, 68, 70]
else:
    tempo = 100
    scale = [60, 62, 64, 65, 67]

# Tempo for all tracks
for t in range(3):
    MyMIDI.addTempo(t, 0, tempo)

# Instrument select (melody track)
if instrument == "piano":
    program = 0
elif instrument == "guitar":
    program = 24
elif instrument == "flute":
    program = 73
else:
    program = 0

MyMIDI.addProgramChange(0, 0, 0, program)   # melody
MyMIDI.addProgramChange(1, 0, 0, 48)        # chords (strings)
MyMIDI.addProgramChange(2, 9, 0, 0)         # drums

time = 0

# 🎼 Chord progression (auto based on scale root)
chords = [
    [scale[0], scale[2], scale[4]],
    [scale[4], scale[6 % len(scale)], scale[1]],
    [scale[5 % len(scale)], scale[0], scale[2]],
    [scale[3], scale[5 % len(scale)], scale[0]]
]

# Generate music
for i in range(8):
    chord = chords[i % len(chords)]

    # chords
    for note in chord:
        MyMIDI.addNote(1, 0, note, time, 2, 70)

    # melody
    for j in range(4):
        note = random.choice(scale)
        MyMIDI.addNote(0, 0, note, time + j * 0.5, 0.5, 100)

    # drums
    MyMIDI.addNote(2, 9, 36, time, 0.5, 100)        # kick
    MyMIDI.addNote(2, 9, 38, time + 0.5, 0.5, 100)  # snare
    MyMIDI.addNote(2, 9, 42, time, 0.25, 80)        # hi-hat
    MyMIDI.addNote(2, 9, 42, time + 0.5, 0.25, 80)

    time += 2

# Save file
with open("pro_output.mid", "wb") as f:
    MyMIDI.writeFile(f)

print("🔥 PRO music generated with choices!")

# Auto play
os.startfile("pro_output.mid")