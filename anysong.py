import telebot
import yt_dlp
import os

# Replace with your Telegram Bot API token from BotFather
TOKEN = '7842155146:AAHjtET6lqzpJyXaEPWWUfv4uCweaisctL4'

bot = telebot.TeleBot(TOKEN)

# Function to download audio from YouTube
def download_audio(youtube_url):
    # yt-dlp options for downloading audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save file in 'downloads' folder
        'quiet': True,
    }
    
    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

# Command handler for the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Any Songs yt Download Bot! Send me a YouTube URL, and I'll send you the audio.")

# Handle user input (YouTube URL) and download audio
@bot.message_handler(func=lambda message: True)
def send_music(message):
    youtube_url = message.text
    
    # Validate the URL
    if 'youtube.com' in youtube_url or 'youtu.be' in youtube_url:
        bot.reply_to(message, "Downloading your song... please wait.")
        try:
            # Download the audio and send it to the user
            audio_file = download_audio(youtube_url)
            bot.send_audio(message.chat.id, open(audio_file, 'rb'))
            os.remove(audio_file)  # Clean up the downloaded file after sending
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Please send a valid YouTube URL.")

# Start the bot
bot.polling()
