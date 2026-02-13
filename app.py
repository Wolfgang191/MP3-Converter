from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

# Render can only reliably write to /tmp
DOWNLOAD_FOLDER = "/tmp"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    youtube_url = request.form.get("youtube_link")

    if not youtube_url:
        return "No URL provided", 400

    output_template = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": "ffmpeg",  # IMPORTANT for Render
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            mp3_file = os.path.splitext(downloaded_file)[0] + ".mp3"

        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return f"Download failed: {str(e)}", 500


if __name__ == "__main__":
    # Local Windows testing only
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
