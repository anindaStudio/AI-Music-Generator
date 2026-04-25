import streamlit as st
from music21 import stream, note, chord, instrument
import random
import time

# 🎨 Page config
st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

# 🎨 Custom CSS
st.markdown("""
<style>
body { background-color: #0e1117; }
.main { background-color: #0e1117; }
h1 { text-align: center; color: #00ffd5; }
.stButton>button {
    background-color: #00ffd5;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #00c9a7;
    color: white;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1f26;
    box-shadow: 0px 0px 10px rgba(0,255,213,0.2);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# 🎵 Title
st.markdown("<h1>🎵 AI Music Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Create music with your mood 🎶</p>", unsafe_allow_html=True)

# 📦 Card UI
st.markdown("<div class='card'>", unsafe_allow_html=True)

mood = st.selectbox("🎭 Select Mood", ["happy", "sad", "chill", "energetic", "romantic"])
instrument_choice = st.selectbox("🎸 Select Instrument", ["piano", "guitar", "flute"])
length = st.slider("🎚️ Music Length", 50, 300, 120)

st.markdown("</div>", unsafe_allow_html=True)

# 🚀 Generate button
if st.button("🚀 Generate Music"):
    with st.spinner("Creating your vibe... 🎧"):

        # 🎯 Mood notes
        if mood == "happy":
            notes_list = ['C4','E4','G4','A4']
        elif mood == "sad":
            notes_list = ['C4','D#4','G4','A#4']
        elif mood == "chill":
            notes_list = ['C4','D4','F4','G4']
        elif mood == "energetic":
            notes_list = ['C4','E4','G4','B4','D5']
        elif mood == "romantic":
            notes_list = ['C4','E4','F4','A4']

        # 🎸 Instrument mapping
        if instrument_choice == "piano":
            selected_instrument = instrument.Piano()
        elif instrument_choice == "guitar":
            selected_instrument = instrument.Guitar()
        elif instrument_choice == "flute":
            selected_instrument = instrument.Flute()

        output_notes = []
        offset = 0

        for i in range(length):
            if random.random() < 0.3:
                chord_notes = [random.choice(notes_list) for _ in range(3)]
                new_chord = chord.Chord(chord_notes)
                new_chord.offset = offset
                new_chord.storedInstrument = selected_instrument
                output_notes.append(new_chord)
            else:
                new_note = note.Note(random.choice(notes_list))
                new_note.offset = offset
                new_note.storedInstrument = selected_instrument
                output_notes.append(new_note)

            offset += 0.5

        filename = f"music_{int(time.time())}.mid"
        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=filename)

        st.success(f"🎶 {mood.capitalize()} music ready! ({instrument_choice})")

        st.audio(filename)

        with open(filename, "rb") as f:
            st.download_button("⬇️ Download Music", f, file_name="music.mid")
