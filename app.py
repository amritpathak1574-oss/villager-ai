import streamlit as st
import yt_dlp
import os
from audio_separator.separator import Separator
from rvc_python.infer import rvc_infer
from pydub import AudioSegment

# 1. Zaroori folders banana (agar pehle se nahi bane hain)
os.makedirs("output", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Streamlit Page Setup
st.set_page_config(page_title="Minecraft Villager AI Cover", page_icon="🎵", layout="centered")
st.title("🤠 Minecraft Villager AI Cover Generator")
st.write("Yeh tool bilkul free aur unlimited hai kyunki yeh aapke local laptop par chalta hai!")

st.markdown("---")

# User Input: YouTube Link
video_url = st.text_input("🔗 Apne manpasand gaane ka YouTube Link yahan dalo:")

# Model file ka path set karna
model_file = "models/villager.pth"

# Check karna ki model folder me hai ya nahi
if not os.path.exists(model_file):
    st.error("⚠️ Mujhe 'models/villager.pth' file nahi mili! Pehle apni extracted file ko 'models' folder me daal kar uska naam 'villager.pth' rakho.")

# Pitch Adjustment Button (Villager ki aawaz thodi bhari ya patli karne ke liye)
pitch_shift = st.slider("🎚️ Pitch Adjust Karo (Singing matching ke liye):", min_value=-12, max_value=12, value=0, step=1)
st.caption("Tip: Agar female song hai toh pitch ko -5 se -12 karo, agar male song hai toh 0 ya thoda badhao.")

st.markdown("---")

# Main Logic Button
if st.button("🚀 Villager Voice Me Convert Karo"):
    if video_url and os.path.exists(model_file):
        
        try:
            # --- STEP 1: YouTube se Audio Download ---
            st.info("📥 YouTube se original audio download ho raha hai...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'output/input_audio.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            st.success("✅ Audio download completed!")
            
            # --- STEP 2: AI se Vocals aur Music Alag Karna ---
            st.info("✂️ AI model se Vocals (Singer) aur Instruments (Music) ko alag kiya ja raha hai...")
            separator = Separator()
            separator.load_model()  # Yeh locally free model background me download karega pehli baar
            
            # Audio split karna
            st.write("Processing audio tracks... Isme 1 minute lag sakta hai.")
            output_files = separator.separate('output/input_audio.wav')
            
            # Standard output paths check karna (audio-separator ke format ke mutabik)
            vocals_path = "output/input_audio_Vocals.wav"
            instruments_path = "output/input_audio_Instruments.wav"
            
            # --- STEP 3: RVC se Villager ki Voice Lagana ---
            st.info("🎤 Villager aapka gaana gaa raha hai... Riyaaz chal raha hai!")
            villager_vocals_path = "output/villager_vocals.wav"
            
            # RVC Infer function bina index file ke run karna
            rvc_infer(
                model_path=model_file,
                index_path="",  # Khali chhoda hai kyunki .index file nahi hai
                input_path=vocals_path,
                output_path=villager_vocals_path,
                f0method="rmvpe",  # Singing ke liye best method
                f0up_key=pitch_shift  
            )
            st.success("✅ Villager ne gaana gaa liya!")
            
            # --- STEP 4: Villager ki Voice aur Music ko Jodna (Merge) ---
            st.info("🎛️ Final mixing chal rahi hai (Music + Villager Voice)...")
            
            music = AudioSegment.from_wav(instruments_path)
            villager_voice = AudioSegment.from_wav(villager_vocals_path)
            
            # Dono audios ko ek ke upar ek mix karna
            final_song = music.overlay(villager_voice)
            final_output_path = "output/villager_final_cover.mp3"
            final_song.export(final_output_path, format="mp3")
            
            # --- STEP 5: Success & Download ---
            st.balloons()
            st.success("🎉 Mubarak ho! Aapka Minecraft Villager Cover taiyar hai!")
            
            # Playable audio player widget
            st.audio(final_output_path, format="audio/mp3")
            
            # Actual Download Button
            with open(final_output_path, "rb") as f:
                st.download_button(
                    label="📥 Final Cover Song Download Karo",
                    data=f,
                    file_name="villager_cover.mp3",
                    mime="audio/mp3"
                )
                
        except Exception as e:
            st.error(f"Kuch gadbad ho gayi bhai: {e}")
            st.info("Tip: Ek baar check karo ki internet chalu hai aur 'models' folder me file sahi se rename hui hai.")
            
    else:
        st.warning("Pehle ya toh YouTube link dalo ya fir models folder me villager.pth file check karo!")
