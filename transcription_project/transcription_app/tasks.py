from celery import shared_task
from .models import Transcription
from whisper import load_model

@shared_task
def transcribe_video_from_url(video_url, transcription_id):
    transcription_instance = Transcription.objects.get(id=transcription_id)
    transcription_instance.status = 'processing'
    transcription_instance.save()

    try:
        # Your existing code for transcription here...
        # Update transcription_instance fields after processing.
        transcription_instance.transcription_text = transcription
        transcription_instance.status = 'completed'
    except Exception as e:
        transcription_instance.status = 'failed'
        transcription_instance.transcription_text = str(e)
    finally:
        transcription_instance.save()
