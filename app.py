
# Zach Schwab
# 2/8/26

import subprocess
import os
import re
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# ffmpeg path
ffmpeg_path = r"C:\Users\zachs\OneDrive\Desktop\prog\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

# folder to store temporary MP3s
TEMP_DIR = os.path.join(os.getcwd(), "temp_downloads")
os.makedirs(TEMP_DIR, exist_ok=True)

def clean_filename(name):
    # Remove characters not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', name)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    youtube_link = request.form.get("youtube_link")

    try:
        output_template = os.path.join(TEMP_DIR, "%(title)s.%(ext)s")

        # Download & convert audio
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", ffmpeg_path,
            "-o", output_template,
            youtube_link
        ], check=True, capture_output=True, text=True)

        # Check folder for file
        files = os.listdir(TEMP_DIR)
        if not files:
            return render_template("index.html", message="No file found!")

        mp3_file = os.path.join(TEMP_DIR, files[-1])
        download_name = clean_filename(files[-1])

        # Send to browser
        return send_file(mp3_file, as_attachment=True, download_name=download_name)

    except subprocess.CalledProcessError as e:
        return render_template("index.html", message=f"Error: {e.stderr}")
    except Exception as e:
        return render_template("index.html", message=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
