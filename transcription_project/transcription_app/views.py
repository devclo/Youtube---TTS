from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transcription
from .serializers import TranscriptionSerializer
from .tasks import transcribe_video_from_url  # We will define this task using Celery.

class TranscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        video_url = request.data.get('video_url')
        transcription_instance = Transcription(video_url=video_url)
        transcription_instance.save()
        
        # Call Celery task
        transcribe_video_from_url.delay(video_url, transcription_instance.id)
        
        return Response(TranscriptionSerializer(transcription_instance).data)
