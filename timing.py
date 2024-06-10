from pyannote.audio import Pipeline
from pydub import AudioSegment
import math

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

def main(fname):
    global pipeline

    duration = AudioSegment.from_wav(fname)
    result = list()

    total_mins = math.ceil(duration.duration_seconds / 60)

    for i in range(0, total_mins, 5):
        t1 = (i) * 60 * 1000
        t2 = (i+5) * 60 * 1000
        split_audio = duration[t1:t2]
        split_audio.export('./output/temp'+str(i)+'.wav', format="wav")
        diarization = pipeline('./output/temp'+str(i)+'.wav')
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            result.append({"start": round(turn.start+(t1/1000), 5), "end": round(turn.end+(t1/1000), 5)})

    temp = list()

    for j in range(len(result)-1):
        if result[j+1]["start"] - result[j]["end"]  >= 3:
            temp.append({"speak1": result[j]["end"], "speak2": result[j+1]["start"]})

    del pipeline  

    return temp, result