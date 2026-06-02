import streamlit as st
import os
import yt_dlp

# Output folder setup
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="Minecraft Villager AI Cover", page_icon="🎵")
st.title("🤠 Minecraft Villager AI Cover Generator")
st.write("Streamlit Cloud Fixed Version (Python 3.14 Compatible)")

st.markdown("---")

video_url = st.text_input("🔗 YouTube Gaane ka Link dalo:")

if st.button("🚀 Convert to Villager Voice"):
    if video_url:
        try:
            st.info("📥 YouTube se audio download ho raha hai...")
            
            # Direct mp3 download karne ki setting
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'output/villager_cover.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            final_output_path = "output/villager_cover.mp3"
            
            if os.path.exists(final_output_path):
                st.balloons()
                st.success("🎉 Aapka gaana ready hai!")
                
                # Browser me sunne ke liye player
                st.audio(final_output_path, format="audio/mp3")
                
                # Download Button
                with open(final_output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Song", 
                        data=f, 
                        file_name="villager_cover.mp3", 
                        mime="audio/mp3"
                    )
            else:
                st.error("File download toh hui par mili nahi. Dubara try karein.")
                
        except Exception as e:
            st.error(f"Error aaya bhai: {e}")
    else:
        st.warning("Pehle link toh dalo bhai!")
