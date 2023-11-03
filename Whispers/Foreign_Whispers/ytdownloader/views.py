from django.shortcuts import render
from django.http import JsonResponse
from .tasks import video_and_captions_download
from .models import Video
from django.views import View

# The view for handling the video download submission
def submit_download(request):
    if request.method == 'POST':
        playlist_url = request.POST.get('playlist_url', '')
        if playlist_url:
            # Trigger the task
            video_and_captions_download.delay(playlist_url)
            return JsonResponse({"status": "Download started"}, status=202)
        else:
            return JsonResponse({"error": "No URL provided"}, status=400)

# The view for displaying the list of videos
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

# The class-based view for the index page
class IndexView(View):
    def get(self, request):
        latest_videos = Video.objects.order_by('-upload_date')[:5]
        return render(request, 'index.html', {'latest_videos': latest_videos})
