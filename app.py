import streamlit as st
import yt_dlp
import os
import urllib.request
from audio_separator.separator import Separator
from rvc_python.infer import rvc_infer
from pydub import AudioSegment

# Cloud par temporary folders banana
os.makedirs("output", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Page Configuration
st.set_page_config(page_title="Minecraft Villager AI Cover", page_icon="🎵")
st.title("🤠 Cloud Minecraft Villager AI Cover Generator")
st.write("Streamlit Cloud par unlimited aur bilkul free!")

st.markdown("---")

# ---- AUTOMATIC MODEL DOWNLOADER ----
# Hugging Face se direct link jahan se model cloud par download hoga
model_url = "https://huggingface.co/Kit_RVC/Minecraft_Villager/resolve/main/Villager.pth"
model_file = "models/villager.pth"

# Agar server par file nahi hai, toh download karega
if not os.path.exists(model_file):
    with st.spinner("📦 Pehli baar setup ho raha hai, Villager AI Model download ho raha hai... (10-15 seconds)"):
        try:
            urllib.request.urlretrieve(model_url, model_file)
            st.success("✅ Villager Model Cloud par download ho gaya!")
        except Exception as e:
            st.error(f"Model download nahi ho paya: {e}")

# User Inputs
video_url = st.text_input("🔗 YouTube Gaane ka Link dalo:")
pitch_shift = st.slider("🎚️ Pitch Adjust Karo (Male song: 0, Female song: -6 se -12):", min_value=-12, max_value=12, value=0, step=1)

st.markdown("---")

# Main Conversion Trigger
if st.button("🚀 Convert to Villager Voice"):
    if video_url and os.path.exists(model_file):
        try:
            # 1. Download Audio from YouTube
            st.info("📥 YouTube se audio download ho raha hai...")
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
            
            # 2. Separate Vocals using AI
            st.info("✂️ AI se Vocals aur Music alag ho rahe hain...")
            separator = Separator()
            separator.load_model() 
            output_files = separator.separate('output/input_audio.wav')
            
            vocals_path = "output/input_audio_Vocals.wav"
            instruments_path = "output/input_audio_Instruments.wav"
            
            # 3. RVC Voice Conversion (Singing to Villager)
            st.info("🎤 Villager aapka gaana gaa raha hai...")
            villager_vocals_path = "output/villager_vocals.wav"
            
            rvc_infer(
                model_path=model_file,
                index_path="",  # Index file ki zarurat nahi hai, bina uske chalega
                input_path=vocals_path,
                output_path=villager_vocals_path,
                f0method="rmvpe",
                f0up_key=pitch_shift
            )
            st.success("✅ Villager ne gaa diya!")
            
            # 4. Mix Villager Voice + Original Background Music
            st.info("🎛️ Final mixing chal rahi hai...")
            music = AudioSegment.from_wav(instruments_path)
            villager_voice = AudioSegment.from_wav(villager_vocals_path)
            
            final_song = music.overlay(villager_voice)
            final_output_path = "output/villager_final_cover.mp3"
            final_song.export(final_output_path, format="mp3")
            
            # 5. Output Preview and Download
            st.balloons()
            st.success("🎉 Aapka Cover taiyar hai!")
            st.audio(final_output_path, format="audio/mp3")
            
            with open(final_output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Song", 
                    data=f, 
                    file_name="villager_cover.mp3", 
                    mime="audio/mp3"
                )
                
        except Exception as e:
            st.error(f"Error aaya bhai: {e}")
            st.info("Tip: Streamlit Cloud ki RAM limited hoti hai, isliye zyada bada gaana mat dalna, 2-3 minute ka gaana best chalega.")
    else:
        st.error("Ya toh link khali hai ya backend me model download nahi hua!")
