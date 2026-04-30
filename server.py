from fastapi import FastAPI, Form
import yt_dlp
import os

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

@app.post("/download")
def download(url: str = Form(...)):

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return {
        "title": info.get("title"),
        "file": file_path
    }
