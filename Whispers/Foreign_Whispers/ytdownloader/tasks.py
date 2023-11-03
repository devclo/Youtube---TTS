# ytdownloader/tasks.py
from celery import shared_task
import yt_dlp as ydlp
import random
import time
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def video_and_captions_download(playlist_url, number_of_videos=10):
    """Download videos and captions from a YouTube playlist and return titles of downloaded videos."""
    downloaded_videos = []

    ydl_opts = {
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
            {"key": "FFmpegSubtitlesConvertor", "format": "srt"},
        ],
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "quiet": False,
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": False,
        "progress_hooks": [my_hook],
        "extract_flat": True,
    }

    with ydlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)

        if "entries" in result:
            videos = result["entries"]
            random.shuffle(videos)
            selected_videos = videos[:number_of_videos]

            for video in selected_videos:
                try:
                    time.sleep(5)
                    logger.info(f'Downloading video: {video["title"]}')
                    ydl.download([video["url"]])
                    downloaded_videos.append(video["title"])
                except Exception as e:
                    logger.error(f"Error downloading video: {video['title']}. Error: {str(e)}")

            logger.info("Download completed!")
        else:
            logger.warning("No entries found in the playlist.")

    return downloaded_videos


def my_hook(d):
    """Hook function to log download progress."""
    if d["status"] == "downloading":
        logger.info(f"Downloading: {d['_percent_str']} % of {d['_total_bytes_str']}")
    if d["status"] == "finished":
        logger.info("Done downloading, now converting ...")


if __name__ == "__main__":
    # This block will only execute if the script is run directly, not when imported
    playlist_url = input("Please enter the YouTube playlist URL: ")
    downloaded = video_and_captions_download(playlist_url)
    for title in downloaded:
        logger.info(f"Downloaded: {title}")
