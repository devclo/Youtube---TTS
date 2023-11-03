from django.urls import path
from .views import submit_download, video_list, IndexView

urlpatterns = [
    # Assuming your app name is 'ytdownloader'
    path('submit-download/', submit_download, name='submit_download'),
    path('videos/', video_list, name='video_list'),
    path('', IndexView.as_view(), name='index'),
]
