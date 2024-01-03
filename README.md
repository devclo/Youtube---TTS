
# YouTube Video to TTS with Subtitles #

## Overview ##

This project uses Streamlit to create a web application that converts YouTube videos into text-to-speech (TTS) audio with subtitles. It supports downloading videos, extracting audio, transcribing the audio, translating subtitles, generating TTS audio, and combining everything into a final video.

## Features ##

* Download YouTube videos.
* Extract audio from the downloaded video.
* Transcribe audio to text.
* Translate subtitles.
* Generate TTS audio using SpeechBrain's Tacotron2 and HIFIGAN models.
* Burn subtitles into the video.
* Combine TTS audio with the video.
## Dependencies ##

* streamlit
* yt_dlp
* ffmpeg
* moviepy
* srt
* torchaudio
* whisper
* speechbrain
* translate (For translation functionalities)

## Installation ##

Save the Script: Copy the content of setup.sh into a file named setup.sh in the root directory of your project.
Give Execution Permission: Before running the script, give it execution permissions. You can do this by running the following command in your terminal:

```bash
chmod +x setup.sh
```

## Usage ##

Run the application

```bash
./setup.sh
```


## Navigate to the provided URL to access the web application. ##

## Functionality ##

1. Video Downloading: Enter a YouTube URL to download the video.
2. Language Selection: Choose the desired language for transcription and subtitles.
3. Audio Extraction and Transcription: The application extracts audio from the video and uses the Whisper model for transcription.
4. Subtitle Translation: Translates the subtitles to the selected language (if different from English).
5. TTS Generation: Generates TTS audio from the transcribed text.
6. Final Video Creation: Combines the video with the TTS audio and subtitles.

# Additional Notes #

Ensure you have a stable internet connection for downloading videos and models.
The translation feature currently supports English to German. More languages can be added by modifying the translate_text function.



## Navigate to the provided URL to access the web application. ##

## Functionality ##

1. Video Downloading: Enter a YouTube URL to download the video.
2. Language Selection: Choose the desired language for transcription and subtitles.
3. Audio Extraction and Transcription: The application extracts audio from the video and uses the Whisper model for transcription.
4. Subtitle Translation: Translates the subtitles to the selected language (if different from English).
5. TTS Generation: Generates TTS audio from the transcribed text.
6. Final Video Creation: Combines the video with the TTS audio and subtitles.

# Additional Notes #

Ensure you have a stable internet connection for downloading videos and models.
The translation feature currently supports English to German. More languages can be added by modifying the translate_text function.


