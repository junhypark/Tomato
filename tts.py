from gtts import gTTS
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import math
from moviepy.editor import VideoFileClip, AudioFileClip

def speed_up(path, speed=1.5):
    audio = AudioSegment.from_file(path)
    ad_audio = audio.speedup(playback_speed=speed)

    return math.ceil(ad_audio.duration_seconds), ad_audio
    
def concat_wav(tts_list, fname, output_path='result.wav'):
    duration = AudioSegment.from_file(fname)
    
    combined_audio = duration[:]

    for t in tts_list:
        t1 = t["start"] * 1000
        t2 = t["end"] * 1000
        
        og_blank = combined_audio[t1:t2]
        blank = AudioSegment.from_file(t["path"])
        speed = 1.4
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
    
    combined_audio.export(output_path, format="wav")

def over_mp4(mp4, wav="./result.wav"):
    video = VideoFileClip(mp4)
    new_audio = AudioFileClip(wav)
    new_audio = new_audio.volumex(1.0)

    video = video.set_audio(new_audio)
    video.write_videofile('./output/result.mp4', codec='libx264', audio_codec='aac')

def main(comment, fname, mp4):
    # comment = [{start, end, text}]
    tts_list = list()

    for cm in comment:
        tts = gTTS(text = cm["text"], lang='ko', slow=False)
        tts.save("comment" + str(cm["start"]) + ".wav")
        tts_list.append({"start": cm["start"], "end": cm["end"], "path": "./comment" + str(cm["start"]) + ".wav"})
    concat_wav(tts_list, fname)
    over_mp4(mp4)
