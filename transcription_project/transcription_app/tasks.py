from celery import shared_task
from .models import Transcription
from whisper import load_model
# You might need additional libraries for handling video and audio extraction
from moviepy.editor import VideoFileClip
import os
import tempfile

@shared_task
def transcribe_video_from_url(video_url, transcription_id):
    transcription_instance = Transcription.objects.get(id=transcription_id)
    transcription_instance.status = 'processing'
    transcription_instance.save()

    try:
        # Assuming a function `download_video` exists
        video_path = download_video(video_url)  # You need to define this function
        clip = VideoFileClip(video_path)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as audio:
            clip.audio.write_audiofile(audio.name)
            clip.close()

            # Load your model (small, medium, or large)
            model = load_model("small")

            # Transcribe the audio file
            result = model.transcribe(audio.name)
            transcription = result['text']

        # Update transcription_instance fields after processing
        transcription_instance.transcription_text = transcription
        transcription_instance.status = 'completed'

        # Optionally, remove the temporary audio file
        os.remove(audio.name)

    except Exception as e:
        transcription_instance.status = 'failed'
        transcription_instance.transcription_text = str(e)

    finally:
        transcription_instance.save()
