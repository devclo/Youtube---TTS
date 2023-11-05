from django.db import models

class Transcription(models.Model):
    video_url = models.URLField(max_length=200)
    transcription_text = models.TextField(blank=True)
    status = models.CharField(max_length=10, default='pending')
    error_message = models.TextField(blank=True)
    # Add any other fields you need for your use case
