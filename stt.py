import whisper

# Whisper 모델 로드
def trans(path):
    model = whisper.load_model("medium")
    
    result = model.transcribe(path, no_speech_threshold=0.6, language='korean')
    
    rawText = result["text"]
    result = reconstruct(result["segments"])
    return rawText, result

def reconstruct(massy):
    # result (list) = {'id': 0,                                                 불필요
    # 'seek': 3000,                                                             불필요
    # 'start': 30.0,                                                            필요
    # 'end': 32.0,                                                              필요
    # 'text': ' 영업 1팀으로 가세요.',                                              필요
    # 'tokens': [50364, 9293, 11534, 502, 169, 3638, 4130, 4147, 7046, 13, 50464], 불?
    # 'temperature': 0.0,                                                       불필요
    # 'avg_logprob': -0.48073904330913836,                                      불필요
    # 'compression_ratio': 0.9747899159663865,                                  불?
    # 'no_speech_prob': 0.037632815539836884}                                   불필요?

    # 일단 start, end, text, no_speech_prob, compression_ratio만 넣어놓음
    # 마지막 두개는 그저 확인용
    result = list()    

    for dic in massy:
        temp = dict()
        temp["start"] = dic["start"]
        temp["end"] = dic["end"]
        temp["text"] = dic["text"]
        temp["com_ratio"] = dic["compression_ratio"]
        temp["no_speech"] = dic["no_speech_prob"]
        result.append(temp)
    
    return result

# 텍스트 정제
def main(path):
    transcribedText, transcribedList = trans(path)
    return transcribedText, transcribedList