import whisper
from pydub import AudioSegment
import os

# wav split with time of pyannote
def split_wav(timestamp, path):
    audio = AudioSegment.from_wav(path)

    result = list()

    for i in timestamp:
        t1 = i["start"] * 1000
        t2 = i["end"] * 1000
        split_audio = audio[t1:t2]
        split_audio.export('temp_wav/temp'+str(t1)+'.wav', format="wav")
        result.append({"path":'temp_wav/temp'+str(t1)+'.wav', "t1": t1/1000, "t2": t2/1000})
        
    return result

# Whisper 모델 로드
def trans(result):
    model = whisper.load_model("medium")
    
    raw_list = list()
    
    for i in result:
        res = model.transcribe(i["path"], no_speech_threshold=0.4, language='korean')
        [raw_list.append({"start": i["t1"], "end": i["t2"], "text": j["text"]}) for j in res["segments"]]
        os.remove(i["path"])

    del model

    return raw_list

# 텍스트 정제
def main(path, timestamp):
    transcribedText= trans(split_wav(timestamp, path))

    return transcribedText