import streamlit as st
from music21 import instrument, note, stream, chord, converter
import numpy as np
import tensorflow as tf
import glob
import random

st.set_page_config(page_title="AI Music Generator")

st.title("🎵 AI Music Generator")
st.write("Generate music using AI (LSTM)")

# 🔥 FIX 1: Sampling function (variation)
def sample(preds, temperature=0.8):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

# 🔥 FIX 2: Cache model (speed up)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("music_model.h5")

model = load_model()

# UI
mood = st.selectbox("Select Mood", ["happy", "sad", "chill", "energetic", "romantic"])
length = st.slider("Music Length", 100, 500, 300)

if st.button("Generate Music 🎶"):
    st.info("Generating... ⏳")

    notes = []

    # Load dataset
    for file in glob.glob("dataset/*.mid"):
        midi = converter.parse(file)

        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    pitchnames = sorted(set(notes))
    n_vocab = len(pitchnames)

    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    sequence_length = 50
    network_input = []

    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])

    # 🔥 FIX 3: Random seed
    pattern = random.choice(network_input)

    prediction_output = []

    for note_index in range(length):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        # 🔥 FIX 4: Random sampling (MAIN FIX)
        index = sample(prediction[0], temperature=0.8)
        result = int_to_note[index]

        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:]

    # Convert to MIDI
    offset = 0
    output_notes = []

    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes_list = []
            for n in notes_in_chord:
                new_note = note.Note(int(n))
                new_note.storedInstrument = instrument.Piano()
                notes_list.append(new_note)
            new_chord = chord.Chord(notes_list)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='ai_output.mid')

    st.success("🎶 Music Generated!")

    st.audio("ai_output.mid")

    with open("ai_output.mid", "rb") as f:
        st.download_button("⬇️ Download Music", f, file_name="ai_music.mid")