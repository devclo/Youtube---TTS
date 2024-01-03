import torchaudio
from speechbrain.pretrained import Tacotron2, HIFIGAN

def setup_tts(tts_dir, vocoder_dir):
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir=tts_dir)
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir=vocoder_dir)
    return tacotron2, hifi_gan

def generate_tts_audio(tacotron2, hifi_gan, text, tts_audio_path):
    mel_output, mel_length, alignment = tacotron2.encode_text(text)
    waveforms = hifi_gan.decode_batch(mel_output)
    torchaudio.save(tts_audio_path, waveforms.squeeze(1), 22050)
