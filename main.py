import streamlit as st
import json
import os
import traceback

st.set_page_config(page_title="#yaw 🎬", layout="wide")
st.title("#yaw 🎬 | Machine Learning Movie Creator")

st.markdown("Upload a movie script and character images to generate a complete AI-generated movie.")

# Safe config loading
try:
    with open("production.json") as f:
        config = json.load(f)
except Exception as e:
    st.warning("⚠️ Using default config due to error loading production.json")
    config = {
        "app_title": "#yaw",
        "description": "AI-powered movie creation from scripts and images."
    }

# Attempt to import modules
try:
    from script_parser import parse_script
    from character_voice import generate_voice_per_scene
    from scene_visualizer import generate_scene_image
    from movie_editor import assemble_full_movie
except Exception as import_error:
    st.error("❌ Failed to load one or more modules.")
    st.code(traceback.format_exc())
    st.stop()

# Upload input
script_file = st.file_uploader("📜 Upload Script (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])
photo_files = st.file_uploader("🖼️ Upload Character Photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

def show_download_link(filepath):
    import base64
    with open(filepath, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
        href = f'<a href="data:video/mp4;base64,{b64}" download="movie_output.mp4">📥 Download Final Movie</a>'
        st.markdown(href, unsafe_allow_html=True)

if script_file and photo_files:
    try:
        os.makedirs("storage", exist_ok=True)
        with st.spinner("📖 Parsing script..."):
            scenes = parse_script(script_file)

        with st.spinner("🗣️ Generating voice clips..."):
            voice_clips = generate_voice_per_scene(scenes)

        with st.spinner("🖼️ Creating scene visuals..."):
            image_clips = generate_scene_image(scenes, photo_files)

        with st.spinner("🎞️ Assembling movie..."):
            final_path = assemble_full_movie(scenes, voice_clips, image_clips)

        st.success("✅ Movie generated!")
        st.video(final_path)
        show_download_link(final_path)

    except Exception as e:
        st.error("⚠️ Something went wrong while generating the movie.")
        st.code(traceback.format_exc())
else:
    st.info("👆 Upload a script and character photos to begin.")

# ✅ End of file — will exit cleanly
