import os
import yt_dlp
from moviepy.editor import VideoFileClip
import subprocess

def download_video(video_url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = ydl.prepare_filename(info_dict)
        return video_title

def extract_audio(video_title, audio_path):
    video_clip = VideoFileClip(video_title)
    video_clip.audio.write_audiofile(audio_path)
    return audio_path

def burn_subtitles(video_path, srt_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles='{srt_path}'",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', '-2',
        output_path
    ]
    subprocess.run(command, check=True)
