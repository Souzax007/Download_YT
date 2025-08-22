# main.py
import yt_dlp
import os

ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")

def baixar_audio(url, pasta_download): 
    os.makedirs(pasta_download, exist_ok=True)
    
    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_download, "%(title)s.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ffmpeg_location': ffmpeg_path
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
