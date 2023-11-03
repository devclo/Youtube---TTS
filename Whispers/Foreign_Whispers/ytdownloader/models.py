from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    status = models.CharField(max_length=50, default='pending')  # could be 'pending', 'downloading', 'completed', 'failed'
    download_path = models.FileField(upload_to='videos/', null=True, blank=True)  # Where the downloaded video will be stored
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    