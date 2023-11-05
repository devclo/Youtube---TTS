# tasks.py in your Django app directory

from celery import shared_task
import os
from moviepy.editor import VideoFileClip
import yt_dlp
import whisper

@shared_task
def sanitize_filename(filename):
    # Replace special characters in filename with an underscore
    return "".join([c if c.isalnum() or c in " .-_" else "_" for c in filename])

@shared_task
def download_video(video_url, output_path='downloads'):
    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Download options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    # Download the video using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        if not os.path.exists(filename):
            # Attempt to fix filename discrepancies
            filename = sanitize_filename(filename)
            if not os.path.exists(filename):
                raise FileNotFoundError(f"The video file {filename} was not found. Download may have failed.")
        return filename

@shared_task
def extract_audio(video_path):
    # Extract audio from video using moviepy
    video_clip = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'  # Change extension to .wav
    video_clip.audio.write_audiofile(audio_path)
    video_clip.close()
    return audio_path

@shared_task
def transcribe_audio(audio_path):
    # Load Whisper model and transcribe audio
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

@shared_task
def transcribe_video_from_url(video_url):
    # Chain the tasks to download, extract audio, and transcribe
    try:
        video_path = download_video(video_url)
        audio_path = extract_audio(video_path)
        transcription = transcribe_audio(audio_path)

        # Cleanup the temporary files
        os.remove(audio_path)
        os.remove(video_path)

        return transcription
    except Exception as e:
        # Log or handle exception appropriately
        raise e
