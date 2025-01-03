from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Aktifkan logging untuk debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi untuk mengirim pesan ulang tahun
async def birthday(update: Update, context: CallbackContext):
    today = datetime.datetime.now().strftime("%m-%d")
    with open('birthdays.json', 'r') as file:
        birthdays = json.load(file)

    # Periksa ulang tahun yang cocok dengan tanggal hari ini
    for name, date in birthdays.items():
        if date[5:] == today:  # format tanggal adalah YYYY-MM-DD
            await update.message.reply_text(f"Selamat ulang tahun, {name}! 🎉🥳")

# Fungsi untuk memulai bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! 😊")

# Fungsi untuk mengirimkan pengingat ulang tahun setiap hari
def send_birthday_reminders():
    today = datetime.datetime.now().strftime("%m-%d")
    with open('birthdays.json', 'r') as file:
        birthdays = json.load(file)

    # Cek ulang tahun hari ini dan kirim pengingat
    for name, date in birthdays.items():
        if date[5:] == today:
            print(f"Selamat ulang tahun, {name}! 🎉🥳")  # Bisa diganti dengan pengiriman pesan ke Telegram

# Fungsi utama untuk menjalankan bot
def main():
    TOKEN = "7910929623:AAFmNzEDXWtRcDA5HPETUKTgFagIEASPlCE"  # Ganti dengan token bot kamu

    # Buat instance aplikasi
    app = Application.builder().token(TOKEN).build()  # Perhatikan penggunaan Application.builder()

    # Tambahkan handler untuk perintah /start dan /birthday
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("birthday", birthday))

    # Setup scheduler untuk mengirim pengingat setiap hari
    scheduler = BackgroundScheduler()

    # Perbaikan untuk menggunakan IntervalTrigger
    scheduler.add_job(send_birthday_reminders, IntervalTrigger(days=1, start_date=datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)), misfire_grace_time=3600)
    scheduler.start()

    # Jalankan bot
    app.run_polling()

if __name__ == "__main__":
    main()
