import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment
import numpy as np
from scipy import signal

st.set_page_config(page_title="Minecraft Villager Singer", page_icon="⛏️")
st.title("⛏️ Minecraft Villager Direct AI Singer")
st.write("Koi bhi YouTube link dalo, app khud hi use Villager ki voice me badal degi!")

# Audio download karne ka function
def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'input_song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return "input_song.mp3"

# Voice ko Villager style me badalne ka function (No API, pure math & audio effects)
def make_it_villager(input_path):
    # Audio load karo
    sound = AudioSegment.from_file(input_path)
    
    # Step 1: Pitch Lowering (Villager ki aawaz bhari hoti hai: "Hrrr")
    # Pitch ko thoda neeche karne ke liye sample rate badlenge
    new_sample_rate = int(sound.frame_rate * 0.75) 
    villager_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    villager_sound = villager_sound.set_frame_rate(44100) # Standard format me wapas laaye
    
    # Step 2: Nasal/Robotic Effect (Villager jaisi "humming" tone ke liye)
    samples = np.array(villager_sound.get_array_of_samples())
    
    # Ek simple sine wave modulation lagayenge jo Villager ki hrrr.. aawaz jaisa vibration de
    fs = villager_sound.frame_rate
    t = np.arange(len(samples)) / fs
    modulation = 1.0 + 0.2 * np.sin(2 * np.pi * 80 * t) # 80Hz ki Villager hum
    
    # Audio samples ko modulat karo
    modulated_samples = samples * modulation
    modulated_samples = np.clip(modulated_samples, -32768, 32767).astype(np.int16)
    
    # Naya audio create karo
    final_sound = villager_sound._spawn(modulated_samples.tobytes())
    
    output_path = "villager_output.mp3"
    final_sound.export(output_path, format="mp3")
    return output_path

# Main UI
song_link = st.text_input("YouTube Link Yahan Dalein:")

if st.button("Villager Voice Me Convert Karo 🚀", type="primary"):
    if song_link:
        try:
            # Step 1: Download
            with st.spinner("🎵 Gaana download ho raha hai..."):
                input_file = download_audio(song_link)
            
            # Step 2: Convert
            with st.spinner("⛏️ Villager aawaz saaf kar raha hai... (Hrrr...)"):
                output_file = make_it_villager(input_file)
            
            # Step 3: Output & Download
            st.success("🎉 Aapka Villager Song Ready Hai!")
            
            # Play Area
            with open(output_file, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            
            # Download Button
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Villager Ka Gaana Download Karo 📥",
                    data=f,
                    file_name="villager_song.mp3",
                    mime="audio/mp3"
                )
                
            # Faltu files delete karne ke liye clean up
            if os.path.exists(input_file): os.remove(input_file)
            if os.path.exists(output_file): os.remove(output_file)
            
        except Exception as e:
            st.error(f"Kuch gadbad hui bhai: {e}")
    else:
        st.warning("Bhai link to dalo pehle!")
