import streamlit as st
from config import *
from video_processing import download_video, extract_audio, burn_subtitles
from text_processing import create_srt_file, translate_srt, extract_text_from_srt
from tts import setup_tts, generate_tts_audio
import whisper

def main():
    st.title("Youtube video to TTS with Subtitles")
    
    tacotron2, hifi_gan = setup_tts(TMP_DIR_TTS, TMP_DIR_VOCODER)

    language = st.selectbox("Select Language for Transcription", ("English", "German"))
    video_url = st.text_input("Enter YouTube Video URL")
    submit_button = st.button("Process Video")

    if submit_button and video_url:
        with st.spinner("Downloading Video..."):
            video_title = download_video(video_url, DOWNLOADS_PATH)

        with st.spinner("Extracting Audio..."):
            audio_path = extract_audio(video_title, AUDIO_PATH)

        with st.spinner("Transcribing Audio..."):
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            english_text = result["text"]

        srt_file_path_en = create_srt_file(english_text, SUBTITLES_PATH)

        if language == "German":
            german_srt_content = translate_srt(extract_text_from_srt(srt_file_path_en), TARGET_LANGUAGE)
            srt_file_path_de = create_srt_file(german_srt_content, SUBTITLES_DE_PATH)
            srt_file_to_use = srt_file_path_de
            text_for_tts = german_srt_content
        else:
            srt_file_to_use = srt_file_path_en
            text_for_tts = english_text

        with st.spinner("Generating TTS Audio..."):
            generate_tts_audio(tacotron2, hifi_gan, text_for_tts, TTS_AUDIO_PATH)

        with st.spinner("Combining Audio with Video..."):
            final_clip = VideoFileClip(video_title).set_audio(AudioFileClip(TTS_AUDIO_PATH))
            final_clip.write_videofile(FINAL_VIDEO_PATH, codec='libx264', audio_codec='aac')
            
        with st.spinner("Burning Subtitles and Combining Audio with Video..."):
            burn_subtitles(video_title, srt_file_to_use, VIDEO_WITH_SUBS_PATH)
            
            final_clip = VideoFileClip(VIDEO_WITH_SUBS_PATH).set_audio(AudioFileClip(TTS_AUDIO_PATH))
            final_clip.write_videofile(FINAL_VIDEO_PATH, codec='libx264', audio_codec='aac')

            st.video(FINAL_VIDEO_PATH)

        with open(FINAL_VIDEO_PATH, 'rb') as f:
            st.download_button(label="Download Video", data=f, file_name=FINAL_VIDEO_PATH, mime="video/mp4")

if __name__ == "__main__":
    main()
