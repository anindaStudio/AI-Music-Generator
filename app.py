import streamlit as st
from music21 import stream, note, chord
import random
import time

st.set_page_config(page_title="AI Music Generator")

st.title("🎵 AI Music Generator (Demo)")
st.write("Generate simple music 🎶")

# UI
length = st.slider("Music Length", 50, 300, 100)

if st.button("Generate Music 🎶"):
    with st.spinner("Generating... ⏳"):

        notes_list = ['C4','D4','E4','F4','G4','A4','B4']

        output_notes = []
        offset = 0

        for i in range(length):
            if random.random() < 0.3:
                # chord
                chord_notes = [random.choice(notes_list) for _ in range(3)]
                new_chord = chord.Chord(chord_notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            else:
                # single note
                new_note = note.Note(random.choice(notes_list))
                new_note.offset = offset
                output_notes.append(new_note)

            offset += 0.5

        # save file
        filename = f"music_{int(time.time())}.mid"
        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=filename)

        st.success("🎶 Music Generated!")

        # play
        st.audio(filename)

        # download
        with open(filename, "rb") as f:
            st.download_button("⬇️ Download Music", f, file_name="music.mid")
