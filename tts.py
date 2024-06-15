from melo.api import TTS
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import math
import re
from moviepy.editor import VideoFileClip, AudioFileClip
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

def decrease_volume(audio, db=10):
    quiter_audio = audio - db

    return quiter_audio

def speed_up(path, speed=1.5):
    audio = AudioSegment.from_file(path)
    ad_audio = audio.speedup(playback_speed=speed)

    return math.ceil(ad_audio.duration_seconds), ad_audio
    
def concat_wav(tts_list, fname, path, output_path='/result.wav'):
    duration = AudioSegment.from_file(fname)
    
    combined_audio = duration[:]

    for t in tts_list:
        t1 = t["start"] * 1000
        t2 = t["end"] * 1000
        
        og_blank = decrease_volume(combined_audio[t1:t2], db=20)
        blank = AudioSegment.from_file(t["path"])
        speed = 1.1
        blank_sec = blank.duration_seconds
        blank_file = blank

        while len(og_blank) < len(blank):
            speed += 0.1
            if len(og_blank) >= blank_sec:
                blank_sec, blank_file = speed_up(t["path"], speed=speed)
                break

        if len(og_blank) >= len(blank_file):
            blank_file = blank_file + AudioSegment.silent(duration=len(og_blank) - len(blank_file))

        overlayed_segment = og_blank.overlay(blank_file)
        
        combined_audio = combined_audio[:t1] + overlayed_segment + combined_audio[t2:]
    
    combined_audio.export(path + output_path, format="wav")

def over_mp4(mp4, path, wav="/result.wav"):
    video = VideoFileClip(mp4)
    new_audio = AudioFileClip(path+wav)
    new_audio = new_audio.volumex(1.0)

    video = video.set_audio(new_audio)
    video.write_videofile(path+'/output/result.mp4', codec='libx264', audio_codec='aac')

def main(comment, fname, mp4, path):
    # comment = [{start, end, text}]
    tts_list = list()

    device = "cuda:0" # or cpu
    speed = 1.1
    model = TTS(language='KR', device=device)
    speaker_ids = model.hps.data.spk2id

    # model loading to revise scenario comment 
    model_path = path+'/train/model'
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
    paraphrase_model = BartForConditionalGeneration.from_pretrained(model_path)
    
    
    for cm in comment:
        # tts = gTTS(text = cm["text"], lang='ko', slow=False)
        # tts.save("comment" + str(cm["start"]) + ".wav")
        wav_path = path+"/comment" + str(cm["start"]) + ".wav"

        inputs = tokenizer(cm["text"], max_length=512, truncation=True, return_tensors="pt")
        output_tokens = paraphrase_model.generate(inputs["input_ids"], max_length=256, num_beams=5, early_stopping=True)
        revised_comment = tokenizer.decode(output_tokens[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        revised_comment = re.sub(r'[\n\r\t]', r' ', revised_comment)
        revised_comment = re.sub(r' +', r' ', revised_comment)

        model.tts_to_file(revised_comment, speaker_ids["KR"], wav_path, speed=speed)
        tts_list.append({"start": cm["start"], "end": cm["end"], "path": path+"/comment" + str(cm["start"]) + ".wav"})

    concat_wav(tts_list, fname, path)
    over_mp4(mp4, path)

if __name__ == '__main__':
    main()