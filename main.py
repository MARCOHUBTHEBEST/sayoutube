import os
import threading
import requests
import yt_dlp
from fastapi import FastAPI, Form
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

# ---------------- FASTAPI PART ----------------

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

    return {"file": file_path}


# ---------------- TELEGRAM BOT ----------------

class Bot:

    def __init__(self):
        app_bot = ApplicationBuilder().token(TOKEN).build()
        app_bot.add_handler(MessageHandler(filters.TEXT, self.handle))
        app_bot.run_polling()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        url = update.message.text

        if "http" not in url:
            await update.message.reply_text("❌ أرسل رابط صحيح")
            return

        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            r = requests.post("http://127.0.0.1:8000/download", data={"url": url})
            file_path = r.json()["file"]

            await update.message.reply_text("📤 جاري الإرسال...")

            await update.message.reply_video(video=open(file_path, "rb"))

        except Exception as e:
            await update.message.reply_text(f"❌ خطأ: {e}")


# ---------------- RUN BOTH ----------------

def run_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_bot():
    Bot()


threading.Thread(target=run_api).start()
run_bot()
