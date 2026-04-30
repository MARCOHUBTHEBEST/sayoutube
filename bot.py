Enterimport requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getgenv("TOKEN")
API_URL = "http://127.0.0.1:8000/download"


class Bot:

    def __init__(self):
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(MessageHandler(filters.TEXT, self.handle))

        app.run_polling()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        url = update.message.text.strip()

        if "http" not in url:
            await update.message.reply_text("❌ أرسل رابط صحيح")
            return

        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            r = requests.post(API_URL, data={"url": url})
            data = r.json()

            file_path = data["file"]

            await update.message.reply_text("📤 جاري الإرسال...")

            await update.message.reply_video(video=open(file_path, "rb"))

        except Exception as e:
            await update.message.reply_text(f"❌ خطأ: {str(e)}")


Bot()
