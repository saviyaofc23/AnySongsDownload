import telebot
import yt_dlp
import os
import re

# Telegram Bot API Token එක ඇතුල් කරන්න
TOKEN = '8040959085:AAHJA4vGcg4zlPQoRZ1ZhOioY09geDqtCOU'
bot = telebot.TeleBot(TOKEN)

# ගීත ඩවුන්ලෝඩ් කිරීම සඳහා ගොනු ගබඩා ස්ථානය
DOWNLOAD_DIR = 'downloads/'

# YouTube වෙතින් අසුර හෝ MP3 එකක් ඩවුන්ලෝඩ් කිරීමේ ක්‍රියාවලිය
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{DOWNLOAD_DIR}%(title)s.%(ext)s',  # 'downloads' ෆෝල්ඩරයට ගොනු සුරැකීම
        'quiet': True,
    }

    try:
        # yt-dlp භාවිතා කර audio එක ඩවුන්ලෝඩ් කරයි
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename
    except Exception as e:
        print(f"Error: {e}")
        return None

# '/start' අණය සඳහා කේතය
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome To Any Songs YouTube Music Download Bot 🎧! Send Me Your YouTube URL.")

# පරිශීලකයාගේ පණිවිඩය සැකසීම
@bot.message_handler(func=lambda message: True)
def download_media(message):
    youtube_url = message.text.strip()

    # YouTube URL එකක් දැක්කා නම්
    if re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.*', youtube_url):
        bot.reply_to(message, "Downloading Content... Please Wait.")

        # ගීත එකක් ඩවුන්ලෝඩ් කිරීම
        audio_file = download_audio(youtube_url)
        if audio_file:
            bot.send_audio(message.chat.id, open(audio_file, 'rb'))
            os.remove(audio_file)  # ගොනුව පවසන්නන්ට පසු මකා දැමීම
        else:
            bot.reply_to(message, "Download Error.")

    else:
        bot.reply_to(message, "Enter Correct YouTube URL.")

# බොට් ආරම්භ කිරීම
bot.polling()
