from django.http import JsonResponse
from .tasks import transcribe_video_from_url

def start_transcription_view(request):
    video_url = request.POST.get('video_url')
    if video_url:
        # This will run the task asynchronously
        task = transcribe_video_from_url.delay(video_url)
        return JsonResponse({'task_id': task.id}, status=202)
    else:
        return JsonResponse({'error': 'No video URL provided'}, status=400)