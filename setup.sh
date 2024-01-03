#!/bin/bash

# Update and install necessary packages
apt install ffmpeg -y
apt update -y
apt upgrade -y

python -m pip install --upgrade pip
pip install streamlit yt-dlp ffmpeg-python moviepy srt torchaudio whisper

# Run the main Python script
python main.py

streamlit run main.py