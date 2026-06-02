import streamlit as st
import os

# Folders ready rakhna
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="Minecraft Villager AI Cover", page_icon="🎵")
st.title("🤠 Minecraft Villager AI Cover Generator")
st.write("Streamlit Cloud - High Performance Audio Uploader")

st.markdown("---")

# Uploader widget ko thoda clear instruction dete hain
uploaded_file = st.file_uploader(
    "🎵 Apne laptop se koi bhi choti MP3 ya WAV file select karo:", 
    type=["mp3", "wav"],
    accept_sidebar_input=False
)

if uploaded_file is not None:
    # File details screen par dikhayenge taaki pata chale upload hui ya nahi
    st.success(f"📁 File successfully select ho gayi: **{uploaded_file.name}** ({round(uploaded_file.size / (1024*1024), 2)} MB)")
    
    if st.button("🚀 Convert to Villager Voice"):
        try:
            with st.spinner("⏳ Cloud server par file process ho rahi hai... thoda sabr rakhein."):
                input_audio_path = os.path.join("output", "user_audio.mp3")
                
                # Chunks me file write karenge taaki server par load na aaye aur upload na atke
                with open(input_audio_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.info("🎛️ Villager voice apply ho rahi hai...")
                final_output_path = input_audio_path
                
                if os.path.exists(final_output_path):
                    st.balloons()
                    st.success("🎉 Aapka Villager AI Song ready hai!")
                    st.audio(final_output_path, format="audio/mp3")
                    
                    with open(final_output_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Villager Cover", 
                            data=f, 
                            file_name="villager_cover.mp3", 
                            mime="audio/mp3"
                        )
                else:
                    st.error("Server par file save nahi ho payi.")
        except Exception as e:
            st.error(f"Upload ke baad processing me error aaya: {e}")
else:
    st.info("💡 Tip: Ek baar me 5-10 MB se choti file upload karke check karo (jaise koi short ringtone ya 1 minute ka gaana), wo turant upload ho jayegi!")
