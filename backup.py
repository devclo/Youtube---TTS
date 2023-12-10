import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import io
import torchaudio
import whisper
from speechbrain.pretrained import Tacotron2, HIFIGAN

# Function to set up the TTS and Vocoder
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def setup_tts():
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")
    return tacotron2, hifi_gan

# Function to download a video
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

# Main function for the Streamlit app
def main():
    st.title("Youtube video to TTS")
    
    # Initialize TTS and Vocoder
    tacotron2, hifi_gan = setup_tts()

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
            text_for_tts = result["text"]
            st.text_area("Transcribed Text", value=text_for_tts, height=300)

        with st.spinner("Generating TTS Audio..."):
            mel_output, mel_length, alignment = tacotron2.encode_text(text_for_tts)
            waveforms = hifi_gan.decode_batch(mel_output)
            tts_audio_path = "tts_audio.wav"
            torchaudio.save(tts_audio_path, waveforms.squeeze(1), 22050)

        with st.spinner("Combining Audio with Video..."):
            tts_audio_clip = AudioFileClip(tts_audio_path)
            final_clip = video_clip.set_audio(tts_audio_clip)
            output_video_path = 'final_video.mp4'
            final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

            st.video(output_video_path)

if __name__ == "__main__":
    main()