import os
import srt
from datetime import timedelta
from translate import Translator

def create_srt_file(text, output_path):
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

def translate_srt(srt_content, target_language):
    translator = Translator(to_lang=target_language)
    translated_srt = []
    for subtitle in srt.parse(srt_content):
        translated_text = translator.translate(subtitle.content)
        translated_subtitle = srt.Subtitle(index=subtitle.index, start=subtitle.start, end=subtitle.end, content=translated_text)
        translated_srt.append(translated_subtitle)
    return srt.compose(translated_srt)

def extract_text_from_srt(srt_file_path):
    with open(srt_file_path, 'r') as file:
        subtitles = list(srt.parse(file.read()))
    return ' '.join([subtitle.content for subtitle in subtitles])
