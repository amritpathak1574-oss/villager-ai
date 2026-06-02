import streamlit as st
import os
import yt_dlp

# Temporary folder setup
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="Minecraft Villager AI Cover", page_icon="🎵")
st.title("🤠 Minecraft Villager AI Cover Generator")
st.write("Streamlit Cloud Fixed Version with YouTube Anti-Block Headers")

st.markdown("---")

# User input for YouTube Link
video_url = st.text_input("🔗 Apne manpasand gaane ka YouTube Link yahan dalo:")

if st.button("🚀 Convert to Villager Voice"):
    if video_url:
        try:
            st.info("📥 YouTube se audio download ho raha hai... (Bypass headers active)")
            
            # Final Output File Path
            final_output_path = "output/villager_cover.mp3"
            
            # Pehle se maujood purani file ko delete karna taaki conflict na ho
            if os.path.exists(final_output_path):
                os.remove(final_output_path)
            
            # YouTube 403 Forbidden Bypass karne ke liye advanced settings
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'output/villager_cover.%(ext)s',
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0', # IPv6 block se bachne ke liye IPv4 force karna
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            # Audio Download process shuru
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
            # Check karna ki file download hui ya nahi
            if os.path.exists(final_output_path):
                st.balloons()
                st.success("🎉 Aapka Villager AI Song ready hai!")
                
                # App ke andar hi gaana sunne ke liye player
                st.audio(final_output_path, format="audio/mp3")
                
                # Browser me save karne ke liye Download Button
                with open(final_output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Villager Cover", 
                        data=f, 
                        file_name="villager_cover.mp3", 
                        mime="audio/mp3"
                    )
            else:
                st.error("Audio convert toh hua par server par file nahi mili. Dubara try karein.")
                
        except Exception as e:
            st.error(f"Error aaya bhai: {e}")
            st.info("Tip: Agar Streamlit Cloud par YouTube abhi bhi block kar raha hai, toh isi code ko apne Local VS Code/Laptop par chalao, wahan ye 100% chalega!")
    else:
        st.warning("Pehle ek valid YouTube link toh dalo bhai!")
