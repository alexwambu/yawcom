# main.py
["main.py"]
content = """
import streamlit as st
import json
import os

try:
    from script_parser import parse_script
    from character_voice import generate_voice_per_scene
    from scene_visualizer import generate_scene_image
    from movie_editor import assemble_full_movie
except ImportError as e:
    st.error(f"🚨 ImportError: {e}")
    st.stop()

try:
    with open("production.json") as f:
        config = json.load(f)
except Exception:
    config = {
        "app_title": "#yaw 🎬 | Movie Generator",
        "description": "Upload a script and character images to generate a full AI movie."
    }

st.set_page_config(page_title=config["app_title"], layout="wide")
st.title(config["app_title"])
st.markdown(config["description"])

script_file = st.file_uploader("📜 Upload Script (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])
photo_files = st.file_uploader("🖼️ Upload Character Photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

def show_download_link(filepath):
    import base64
    with open(filepath, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
        href = f'<a href="data:video/mp4;base64,{b64}" download="movie_output.mp4">📥 Download Final Movie</a>'
        st.markdown(href, unsafe_allow_html=True)

if script_file and photo_files:
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
else:
    st.info("👆 Upload a script and character photos to get started.")
"""

# movie_editor.py
["movie_editor.py"]
content = """
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
import os

def assemble_full_movie(scenes, voice_clips, image_clips):
    clips = []
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    for i in range(len(scenes)):
        img = ImageClip(image_clips[i]).set_duration(10)
        scene_label = f"({chr(97 + i)})"

        try:
            txt_clip = TextClip(scene_label, fontsize=40, color='white', font=FONT_PATH)
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(10)
        except Exception as e:
            print(f"TextClip error: {e}")
            txt_clip = None

        video = CompositeVideoClip([img, txt_clip] if txt_clip else [img])
        audio = AudioFileClip(voice_clips[i])
        video = video.set_audio(audio)
        clips.append(video)

    movie = concatenate_videoclips(clips, method="compose")
    output_path = "storage/final_movie.mp4"
    movie.write_videofile(output_path, fps=24)
    return output_path
"""

# script_parser.py
["script_parser.py"]
content = """
import docx
import PyPDF2

def parse_script(file):
    if file.name.endswith(".txt"):
        text = file.read().decode()
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = "\\n".join([p.text for p in doc.paragraphs])
    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = "\\n".join([page.extract_text() for page in reader.pages])
    else:
        return []

    raw_scenes = text.split("Scene")
    scenes = [{"id": i, "text": s.strip()} for i, s in enumerate(raw_scenes) if len(s.strip()) > 10]
    return scenes
"""

# character_voice.py
["character_voice.py"]
content = """
from gtts import gTTS
import os

def generate_voice_per_scene(scenes):
    voice_paths = []
    os.makedirs("storage", exist_ok=True)

    for scene in scenes:
        speech = scene['text'][:500]
        tts = gTTS(speech)
        path = f"storage/voice_{scene['id']}.mp3"
        tts.save(path)
        voice_paths.append(path)

    return voice_paths
"""

# scene_visualizer.py
["scene_visualizer.py"]
content = """
from PIL import Image
import io
import os

def generate_scene_image(scenes, uploaded_images):
    os.makedirs("storage", exist_ok=True)
    images = []

    for i, scene in enumerate(scenes):
        img_index = i % len(uploaded_images)
        img_bytes = uploaded_images[img_index].read()
        img = Image.open(io.BytesIO(img_bytes)).resize((1280, 720))
        img_path = f"storage/scene_{scene['id']}.png"
        img.save(img_path)
        images.append(img_path)

    return images
"""

# utils.py
["utils.py"]
content = """
import os

def ensure_storage_dir():
    os.makedirs("storage", exist_ok=True)
"""

# production.json
["production.json"]
content = """
{
  "app_title": "#yaw 🎬 | Machine Learning Movie Creator",
  "description": "Upload a script and character images to generate a complete AI-generated movie with unique voices and scenes."
}
"""

# requirements.txt
["requirements.txt"]
content = """
streamlit
moviepy
gtts
pillow
python-docx
PyPDF2
"""

# packages.txt
["packages.txt"]
content = """
ffmpeg
fonts-dejavu-core
"""

# README.md
["README.md"]
content = """
# 🎬 #yaw - Machine Learning Movie Creator

Upload a movie script and character photos to generate a fully AI-edited movie in `.mp4` format.

## ✅ Features

- Parses scripts into scenes
- Generates per-character voice using `gTTS`
- Maps scenes visually using user-uploaded images
- Creates final video with `moviepy`

---

## 🚀 How to Run

### Local

```bash
pip install -r requirements.txt
streamlit run main.py
