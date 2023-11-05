from django.db import models

class Transcription(models.Model):
    video_url = models.URLField()
    transcription_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed
