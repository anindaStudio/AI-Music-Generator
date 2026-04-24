from music21 import converter, instrument, note, chord
import glob
import numpy as np

notes = []

# 🔹 STEP 1: Load all MIDI files
for file in glob.glob("dataset/*.mid"):
    print("Reading:", file)
    midi = converter.parse(file)

    parts = instrument.partitionByInstrument(midi)

    if parts:
        notes_to_parse = parts.parts[0].recurse()
    else:
        notes_to_parse = midi.flat.notes

    # 🔹 STEP 2: Extract notes & chords
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

# 🔹 STEP 3: Summary
print("Total notes:", len(notes))

# 🔹 STEP 4: Create sequence (for AI training)
sequence_length = 50

pitchnames = sorted(set(notes))
n_vocab = len(pitchnames)

print("Unique notes:", n_vocab)

# Map notes to numbers
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

network_input = []
network_output = []

for i in range(0, len(notes) - sequence_length):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]

    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])

n_patterns = len(network_input)

print("Total patterns:", n_patterns)

# 🔹 STEP 5: Reshape input
network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))

# Normalize input
network_input = network_input / float(n_vocab)

print("Data ready for training!")