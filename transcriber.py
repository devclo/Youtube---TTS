import streamlit as st
from translate import Translator
import yt_dlp
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import srt
from datetime import timedelta
import torchaudio
import subprocess
import whisper
from speechbrain.pretrained import Tacotron2, HIFIGAN

# Function to set up the TTS and Vocoder
@st.cache_resource
def setup_tts():
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")
    return tacotron2, hifi_gan


def download_video(video_url, output_path='downloads'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = ydl.prepare_filename(info_dict)
        return video_title

def create_srt_file(text, output_path='subtitles.srt'):
    sentences = text.split('. ')
    srt_entries = []
    start_time = timedelta(seconds=0)
    for i, sentence in enumerate(sentences):
        end_time = start_time + timedelta(seconds=len(sentence) / 5)
        entry = srt.Subtitle(index=i+1, start=start_time, end=end_time, content=sentence)
        srt_entries.append(entry)
        start_time = end_time + timedelta(seconds=1)

    srt_content = srt.compose(srt_entries)
    with open(output_path, 'w') as file:
        file.write(srt_content)

    return output_path

def translate_srt(srt_content, target_language='de'):
    translator = Translator(to_lang=target_language)
    translated_srt = []
    for subtitle in srt.parse(srt_content):
        translated_text = translator.translate(subtitle.content)
        translated_subtitle = srt.Subtitle(index=subtitle.index, start=subtitle.start, end=subtitle.end, content=translated_text)
        translated_srt.append(translated_subtitle)
    return srt.compose(translated_srt)


def burn_subtitles(video_path, srt_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles='{srt_path}'",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', '-2',
        output_path
    ]
    subprocess.run(command, check=True)
    
def translate_text(text, target_language='de'):
    # Translate text from English to the target language (default is German)
    translator = Translator(to_lang=target_language)
    translated_text = []

    # Split the text into chunks of 500 characters
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Translate each chunk and append to the translated_text list
    for chunk in chunks:
        translated_chunk = translator.translate(chunk)
        translated_text.append(translated_chunk)

    # Join the translated chunks
    return ' '.join(translated_text)

def extract_text_from_srt(srt_file_path):
    with open(srt_file_path, 'r') as file:
        subtitles = list(srt.parse(file.read()))
    return ' '.join([subtitle.content for subtitle in subtitles])

def main():
    st.title("Youtube video to TTS with Subtitles")
    
    tacotron2, hifi_gan = setup_tts()

    language = st.selectbox("Select Language for Transcription", ("English", "German"))
    video_url = st.text_input("Enter YouTube Video URL")
    submit_button = st.button("Process Video")

    if submit_button and video_url:
        with st.spinner("Downloading Video..."):
            video_title = download_video(video_url)

        with st.spinner("Extracting Audio..."):
            video_clip = VideoFileClip(video_title)
            audio_path = "video_audio.wav"
            video_clip.audio.write_audiofile(audio_path)

        with st.spinner("Transcribing Audio..."):
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            english_text = result["text"]

        srt_file_path_en = create_srt_file(english_text)

        if language == "German":
            with open(srt_file_path_en, "r") as file:
                english_srt_content = file.read()
            german_srt_content = translate_srt(english_srt_content)
            srt_file_path_de = create_srt_file(german_srt_content, output_path='subtitles_de.srt')
            srt_file_to_use = srt_file_path_de
            text_for_tts = german_srt_content
        else:
            srt_file_to_use = srt_file_path_en
            text_for_tts = english_text

        with st.spinner("Generating TTS Audio..."):
            mel_output, mel_length, alignment = tacotron2.encode_text(text_for_tts)
            waveforms = hifi_gan.decode_batch(mel_output)
            tts_audio_path = "tts_audio.wav"
            torchaudio.save(tts_audio_path, waveforms.squeeze(1), 22050)

        with st.spinner("Combining Audio with Video..."):
            tts_audio_clip = AudioFileClip(tts_audio_path)
            final_clip = video_clip.set_audio(tts_audio_clip)
            output_video_path = 'final_video.mp4'
            final_clip.write_videofile(output_video_path, codec
                                       ='libx264', audio_codec='aac')
            
        with st.spinner("Burning Subtitles and Combining Audio with Video..."):
            # Create a temporary video file path to burn subtitles
            video_with_subs_path = 'video_with_subs.mp4'
            # Burn the subtitles onto the video
            burn_subtitles(video_title, srt_file_to_use, video_with_subs_path)
            
            # Load the video with subtitles
            video_with_subs_clip = VideoFileClip(video_with_subs_path)
            # Set the TTS audio on the video with subtitles
            final_clip = video_with_subs_clip.set_audio(AudioFileClip(tts_audio_path))
            output_video_path = 'final_video.mp4'
            final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

            # Display the final video with subtitles and TTS audio
            st.video(output_video_path)    



        with open("final_video.mp4", 'rb') as f:
            st.download_button(label="Download Video", data=f, file_name="final_video.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()