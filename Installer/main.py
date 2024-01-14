import telebot
import youtube_dl
from pytube import YouTube
import instaloader
import os
import requests
from datetime import datetime
import time

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Можешь скинуть мне ссылку на видео.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        url = message.text
        if 'youtube.com' in url:
            download_youtube_video(message)
        else:
            bot.send_message(message.chat.id, "Извините, не могу обработать данную ссылку.")
    except Exception as e:
        print(f"Ошибка обработки сообщения: {str(e)}")

def download_youtube_video(message):
    start = datetime.now()
    yt_url = message.text
    yt = YouTube(yt_url)
    video = yt.streams.filter(file_extension='mp4').first()
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    current_datetime = current_datetime.replace(' ', '_')
    video_path = os.path.abspath(os.path.join('./downloads', f"{current_datetime}.mp4"))
    os.makedirs('./downloads', exist_ok=True)
    video.download(output_path='./downloads', filename=current_datetime + ".mp4")
    with open(video_path, 'rb') as video_file:
        bot.send_video(message.chat.id, video_file)
    stop = datetime.now()
    count = stop-start
    bot.send_message(message.chat.id, f"Время оброботки: {count}")
    time.sleep(2)

if __name__ == "__main__":
    bot.polling(none_stop=True)
