import streamlit as st
from music21 import stream, note, chord
import random
import time

st.set_page_config(page_title="AI Music Generator")

st.title("🎵 AI Music Generator")
st.write("Create music with your choice 🎶")

# 🎯 NEW: Mood selection
mood = st.selectbox("Select Mood", ["happy", "sad", "chill"])

# 🎯 NEW: Instrument selection (UI only for now)
instrument = st.selectbox("Select Instrument", ["piano", "guitar", "flute"])

# 🎯 Length
length = st.slider("Music Length", 50, 300, 100)

if st.button("Generate Music 🎶"):
    with st.spinner("Generating... ⏳"):

        # 🎯 Mood based notes
        if mood == "happy":
            notes_list = ['C4','E4','G4','A4']
        elif mood == "sad":
            notes_list = ['C4','D#4','G4','A#4']
        else:
            notes_list = ['C4','D4','F4','G4']

        output_notes = []
        offset = 0

        for i in range(length):
            if random.random() < 0.3:
                chord_notes = [random.choice(notes_list) for _ in range(3)]
                new_chord = chord.Chord(chord_notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            else:
                new_note = note.Note(random.choice(notes_list))
                new_note.offset = offset
                output_notes.append(new_note)

            offset += 0.5

        filename = f"music_{int(time.time())}.mid"
        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=filename)

        st.success(f"🎶 Music Generated! ({mood} mood, {instrument})")

        st.audio(filename)

        with open(filename, "rb") as f:
            st.download_button("⬇️ Download Music", f, file_name="music.mid")
